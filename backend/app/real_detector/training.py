"""Training + honest evaluation.

The dataset holds one row per REGISTERED DOMAIN, and splits are grouped by domain, so the test
set only contains domains the model never saw in training.
"""
from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, f1_score, precision_recall_curve, roc_auc_score, roc_curve
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .features import CAT_COLUMNS, NUMERIC_COLUMNS, features_frame, normalize_host, registered_domain

SEED = 42
MODEL_VERSION = "1.1"
BLOCK_MAX_FPR = 0.05  # "PHISHING" verdict must keep false positives <= 5% on validation data


# --------------------------------------------------------------------------- data
def load_dataset(path: Path) -> pd.DataFrame:
    """CSV with columns host,label -> one row per registered domain (label 1 = phishing)."""
    df = pd.read_csv(path)
    if not {"host", "label"} <= set(df.columns):
        raise ValueError("dataset must have columns: host,label (1 = phishing, 0 = legitimate)")
    doms: List[str] = []
    labels: List[int] = []
    for h, y in zip(df["host"].astype(str), df["label"].astype(int)):
        try:
            doms.append(registered_domain(normalize_host(h)))
            labels.append(int(y))
        except ValueError:
            continue
    out = pd.DataFrame({"host": doms, "label": labels})
    # a domain that appears with both labels is ambiguous -> drop it entirely
    conflict = out.groupby("host")["label"].nunique()
    out = out[~out["host"].isin(conflict[conflict > 1].index)].drop_duplicates("host")
    out["group"] = out["host"]
    return out.reset_index(drop=True)


def group_split(df: pd.DataFrame, test_size: float, seed: int = SEED) -> Tuple[pd.DataFrame, pd.DataFrame]:
    gss = GroupShuffleSplit(n_splits=1, test_size=test_size, random_state=seed)
    tr, te = next(gss.split(df, df["label"], groups=df["group"]))
    return df.iloc[tr].reset_index(drop=True), df.iloc[te].reset_index(drop=True)


# --------------------------------------------------------------------------- models
def _preprocessor(with_ngrams: bool) -> ColumnTransformer:
    cat = ("tld", OneHotEncoder(handle_unknown="ignore", min_frequency=10), CAT_COLUMNS)
    if with_ngrams:
        return ColumnTransformer([
            ("ngram", TfidfVectorizer(analyzer="char", ngram_range=(2, 5), min_df=3,
                                      max_features=100_000, sublinear_tf=True), "host"),
            ("num", StandardScaler(), NUMERIC_COLUMNS),
            cat,
        ])
    return ColumnTransformer([("num", "passthrough", NUMERIC_COLUMNS), cat])


def build_candidates() -> Dict[str, Pipeline]:
    return {
        "logreg_ngrams_plus_features": Pipeline([
            ("prep", _preprocessor(True)),
            ("clf", LogisticRegression(C=4.0, max_iter=3000, random_state=SEED)),
        ]),
        "random_forest_features_only": Pipeline([
            ("prep", _preprocessor(False)),
            ("clf", RandomForestClassifier(n_estimators=300, min_samples_leaf=2,
                                           n_jobs=-1, random_state=SEED)),
        ]),
    }


def heuristic_baseline(frame: pd.DataFrame) -> np.ndarray:
    """Hand-written rules a beginner might use. Must be beaten by the trained model."""
    rule = (
        (frame["is_ip"] == 1)
        | (frame["n_hyphens"] >= 2)
        | (frame["length"] > 30)
        | (frame["kw_count"] >= 1)
        | (frame["max_digit_run"] >= 5)
    )
    return rule.astype(float).to_numpy()


# --------------------------------------------------------------------------- metrics
def best_threshold(y_true: np.ndarray, p: np.ndarray) -> float:
    prec, rec, thr = precision_recall_curve(y_true, p)
    f1 = 2 * prec[:-1] * rec[:-1] / np.clip(prec[:-1] + rec[:-1], 1e-12, None)
    return float(thr[int(np.argmax(f1))]) if len(thr) else 0.5


def threshold_for_fpr(y_true: np.ndarray, p: np.ndarray, max_fpr: float) -> float:
    """Lowest threshold whose false-positive rate is <= max_fpr (i.e. the highest recall allowed)."""
    fpr, _tpr, thr = roc_curve(y_true, p)
    ok = np.where(fpr <= max_fpr)[0]
    i = int(ok[-1]) if len(ok) else 0
    t = float(thr[i])
    return t if np.isfinite(t) else 1.0


def metrics_at(y_true: np.ndarray, p: np.ndarray, thr: float) -> Dict[str, Any]:
    pred = (p >= thr).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, pred, labels=[0, 1]).ravel()
    precision = tp / max(tp + fp, 1)
    recall = tp / max(tp + fn, 1)
    try:
        auc = float(roc_auc_score(y_true, p))
    except ValueError:
        auc = float("nan")
    return {
        "threshold": round(float(thr), 4),
        "precision": round(float(precision), 4),
        "recall": round(float(recall), 4),
        "f1": round(float(f1_score(y_true, pred, zero_division=0)), 4),
        "fpr": round(float(fp / max(fp + tn, 1)), 4),
        "accuracy": round(float((tp + tn) / len(y_true)), 4),
        "roc_auc": round(auc, 4),
        "tp": int(tp), "fp": int(fp), "tn": int(tn), "fn": int(fn),
    }


# --------------------------------------------------------------------------- pipeline
def run_training(df: pd.DataFrame, out_dir: Path, dataset_info: Dict[str, Any] | None = None,
                 test_size: float = 0.2, seed: int = SEED) -> Dict[str, Any]:
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
    except OSError:
        pass

    train_full, test = group_split(df, test_size, seed)
    train, val = group_split(train_full, 0.2, seed)

    Xtr, Xva, Xte, Xtf = (features_frame(d["host"].tolist()) for d in (train, val, test, train_full))
    ytr, yva, yte, ytf = (d["label"].to_numpy() for d in (train, val, test, train_full))

    # 1) pick the best candidate (and its threshold) using the VALIDATION set only
    selection: Dict[str, Dict[str, Any]] = {}
    for name, pipe in build_candidates().items():
        pipe.fit(Xtr, ytr)
        pv = pipe.predict_proba(Xva)[:, 1]
        thr = best_threshold(yva, pv)
        selection[name] = {
            "val_f1": metrics_at(yva, pv, thr)["f1"],
            "threshold": thr,                                    # max-F1 point -> "review"
            "threshold_block": threshold_for_fpr(yva, pv, BLOCK_MAX_FPR),  # FPR <= 5% -> "block"
        }
    best_name = max(selection, key=lambda n: selection[n]["val_f1"])
    thr = selection[best_name]["threshold"]
    thr_block = selection[best_name]["threshold_block"]

    # 2) refit every candidate on train+val, evaluate ONCE on the untouched test set
    rows: Dict[str, Dict[str, Any]] = {}
    fitted: Dict[str, Pipeline] = {}
    for name, pipe in build_candidates().items():
        pipe.fit(Xtf, ytf)
        fitted[name] = pipe
        pt = pipe.predict_proba(Xte)[:, 1]
        rows[name] = metrics_at(yte, pt, selection[name]["threshold"])
    rows["heuristic_rules_baseline"] = metrics_at(yte, heuristic_baseline(Xte), 0.5)
    final = fitted[best_name]
    p_final = final.predict_proba(Xte)[:, 1]
    operating_points = {
        "review_max_f1": metrics_at(yte, p_final, thr),
        "block_fpr_le_5pct": metrics_at(yte, p_final, thr_block),
    }
    test_metrics = operating_points["block_fpr_le_5pct"]

    trained_at = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    bundle = {
        "pipeline": final,
        "threshold": float(thr_block),          # >= this -> PHISHING
        "threshold_review": float(thr),         # >= this -> SUSPICIOUS
        "version": MODEL_VERSION,
        "trained_at": trained_at,
        "model_name": best_name,
        "sklearn_version": sklearn.__version__,
        "test_metrics": {k: test_metrics[k] for k in ("precision", "recall", "f1", "fpr", "roc_auc")},
    }
    joblib.dump(bundle, out_dir / "url_model.joblib", compress=3)

    report = {
        "trained_at": trained_at,
        "sklearn_version": sklearn.__version__,
        "dataset": {
            "rows": int(len(df)), "phishing": int(df["label"].sum()),
            "legitimate": int((df["label"] == 0).sum()),
            "train_rows": int(len(train_full)), "test_rows": int(len(test)),
            "test_unique_registered_domains": int(test["group"].nunique()),
            **(dataset_info or {}),
        },
        "selected_model": best_name,
        "validation_selection": selection,
        "test_strict_domain_split": rows,
        "operating_points_shipped_model": operating_points,
    }
    (out_dir / "metrics.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


# --------------------------------------------------------------------------- report text
def _pct(x: float) -> str:
    return f"{x * 100:.2f}%"


def results_markdown(report: Dict[str, Any]) -> str:
    d = report["dataset"]
    lines = [
        f"_Trained {report['trained_at']} - scikit-learn {report['sklearn_version']} - "
        f"{d['rows']:,} hosts ({d['phishing']:,} phishing / {d['legitimate']:,} legitimate). "
        f"Test set: {d['test_rows']:,} hosts from {d['test_unique_registered_domains']:,} registered domains "
        "that never appear in training._",
        "",
        "| Model (held-out domains) | Precision | Recall | F1 | False-positive rate | ROC-AUC |",
        "|---|---|---|---|---|---|",
    ]
    names = {
        "logreg_ngrams_plus_features": "Logistic Regression (char n-grams + features)",
        "random_forest_features_only": "Random Forest (features only)",
        "heuristic_rules_baseline": "Hand-written rules (baseline)",
    }
    for key, m in report["test_strict_domain_split"].items():
        star = " **(shipped)**" if key == report["selected_model"] else ""
        lines.append(f"| {names.get(key, key)}{star} | {_pct(m['precision'])} | {_pct(m['recall'])} | "
                     f"{_pct(m['f1'])} | {_pct(m['fpr'])} | {m['roc_auc']:.4f} |")
    op = report["operating_points_shipped_model"]
    lines += [
        "",
        "How the shipped model is used (two thresholds chosen on validation data, measured on the test set):",
        "",
        "| Verdict | Rule | Precision | Recall | False-positive rate |",
        "|---|---|---|---|---|",
        f"| PHISHING | score >= {op['block_fpr_le_5pct']['threshold']:.2f} (tuned for FPR <= 5%) | "
        f"{_pct(op['block_fpr_le_5pct']['precision'])} | {_pct(op['block_fpr_le_5pct']['recall'])} | "
        f"{_pct(op['block_fpr_le_5pct']['fpr'])} |",
        f"| SUSPICIOUS or worse | score >= {op['review_max_f1']['threshold']:.2f} (max F1) | "
        f"{_pct(op['review_max_f1']['precision'])} | {_pct(op['review_max_f1']['recall'])} | "
        f"{_pct(op['review_max_f1']['fpr'])} |",
    ]
    lines += [
        "",
        "**Read these numbers with care:** the legitimate class mixes popular domains with random everyday "
        "domains, but real traffic contains many more kinds of legitimate sites, so real-world false positives "
        "are likely higher than shown. The model judges the registered domain only (not the page, path or content), "
        "and it cannot judge individual sites hosted on shared platforms (github.io, netlify.app, ...).",
    ]
    return "\n".join(lines)


def update_readme(readme: Path, markdown: str) -> bool:
    if not readme.exists():
        return False
    text = readme.read_text(encoding="utf-8")
    pattern = re.compile(r"(<!-- RESULTS:START -->)(.*?)(<!-- RESULTS:END -->)", re.S)
    if not pattern.search(text):
        return False
    readme.write_text(pattern.sub(lambda m: f"{m.group(1)}\n{markdown}\n{m.group(3)}", text), encoding="utf-8")
    return True
