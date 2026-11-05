import json

import joblib
import numpy as np

from app.real_detector.features import registered_domain
from app.real_detector.training import (
    group_split, load_dataset, metrics_at, results_markdown, threshold_for_fpr, update_readme,
)
from helpers import synthetic_frame


def test_dataset_is_collapsed_to_registered_domains_and_conflicts_dropped(tmp_path):
    csv = tmp_path / "d.csv"
    csv.write_text(
        "host,label\n"
        "a.evil.xyz,1\nb.evil.xyz,1\n"          # same registered domain -> 1 row
        "good.com,0\nwww.good.com,0\n"           # same -> 1 row
        "mixed.net,1\nmixed.net,0\n"             # label conflict -> dropped
        "javascript:alert(1),1\n",               # unusable -> skipped
        encoding="utf-8",
    )
    df = load_dataset(csv)
    assert sorted(df["host"]) == ["evil.xyz", "good.com"]


def test_group_split_never_shares_a_domain():
    df = load_dataset_from_frame()
    train, test = group_split(df, 0.2)
    assert set(train["group"]).isdisjoint(set(test["group"]))
    assert len(test) > 0 and len(train) > len(test)


def load_dataset_from_frame():
    df = synthetic_frame(120)
    df["host"] = df["host"].map(registered_domain)
    df["group"] = df["host"]
    return df


def test_training_writes_artifacts_and_honest_metrics(tiny_model_dir):
    assert (tiny_model_dir / "url_model.joblib").exists()
    report = json.loads((tiny_model_dir / "metrics.json").read_text())
    assert {"selected_model", "test_strict_domain_split", "operating_points_shipped_model"} <= set(report)
    assert "heuristic_rules_baseline" in report["test_strict_domain_split"]
    bundle = joblib.load(tiny_model_dir / "url_model.joblib")
    assert bundle["threshold"] >= bundle["threshold_review"]
    md = results_markdown(report)
    assert "False-positive rate" in md and "Read these numbers with care" in md


def test_metrics_math():
    y = np.array([1, 1, 0, 0])
    p = np.array([0.9, 0.4, 0.6, 0.1])
    m = metrics_at(y, p, 0.5)
    assert (m["tp"], m["fp"], m["tn"], m["fn"]) == (1, 1, 1, 1)
    assert m["precision"] == 0.5 and m["recall"] == 0.5 and m["fpr"] == 0.5


def test_threshold_for_fpr_respects_the_cap():
    rng = np.random.default_rng(0)
    y = np.array([0] * 500 + [1] * 500)
    p = np.concatenate([rng.beta(2, 6, 500), rng.beta(6, 2, 500)])
    thr = threshold_for_fpr(y, p, 0.05)
    assert metrics_at(y, p, thr)["fpr"] <= 0.05


def test_update_readme_replaces_only_the_marked_block(tmp_path):
    readme = tmp_path / "README.md"
    readme.write_text("intro\n<!-- RESULTS:START -->\nold\n<!-- RESULTS:END -->\noutro\n", encoding="utf-8")
    assert update_readme(readme, "NEW TABLE")
    text = readme.read_text(encoding="utf-8")
    assert "NEW TABLE" in text and "old" not in text and text.startswith("intro") and text.rstrip().endswith("outro")
    assert update_readme(tmp_path / "missing.md", "x") is False
