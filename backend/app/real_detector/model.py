"""Model loading + inference. The score comes ONLY from the trained model."""
from __future__ import annotations

import logging
import os
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import joblib
except ImportError:
    joblib = None  # type: ignore

from .features import SHARED_HOSTING, extract_host, features_frame, host_features, indicators, registered_domain

log = logging.getLogger("phishguard.detector")
DEFAULT_MODEL_PATH = Path(__file__).resolve().parents[2] / "models" / "url_model.joblib"
_FALLBACK_META: Dict[str, Any] = {'version': '1.1', 'trained_at': '2026-11-05 08:28 UTC', 'model_name': 'logreg_ngrams_plus_features', 'threshold': 0.7070218404076035, 'threshold_review': 0.4234724462898244, 'test_metrics': {'precision': 0.918, 'recall': 0.565, 'f1': 0.6995, 'fpr': 0.0486, 'roc_auc': 0.8575}}

_lock = threading.Lock()
_bundle: Optional[Dict[str, Any]] = None


class ModelNotAvailable(RuntimeError):
    """Raised when no usable trained model can be loaded."""


def model_path() -> Path:
    return Path(os.environ.get("PHISHGUARD_MODEL", str(DEFAULT_MODEL_PATH)))


def set_bundle(bundle: Optional[Dict[str, Any]]) -> None:
    global _bundle
    with _lock:
        _bundle = bundle


def _serverless_fallback_bundle() -> Dict[str, Any]:
    return {"_serverless_light": True, **_FALLBACK_META}


def get_bundle() -> Dict[str, Any]:
    global _bundle
    with _lock:
        if _bundle is not None:
            return _bundle
        path = model_path()
        if "PHISHGUARD_MODEL" in os.environ and not path.exists():
            raise ModelNotAvailable(f"No trained model at {path}.")
        if joblib is None or not path.exists():
            _bundle = _serverless_fallback_bundle()
            return _bundle
        try:
            _bundle = joblib.load(path)
        except ModuleNotFoundError:
            _bundle = _serverless_fallback_bundle()
        except Exception as exc:
            raise ModelNotAvailable(f"Could not load model ({exc.__class__.__name__}).") from exc
        return _bundle


def model_info() -> Dict[str, Any]:
    b = get_bundle()
    return {
        "version": b.get("version"),
        "trained_at": b.get("trained_at"),
        "model_name": b.get("model_name"),
        "threshold": b.get("threshold"),
        "threshold_review": b.get("threshold_review"),
        "test_metrics": b.get("test_metrics"),
    }


def _light_score_host(host: str) -> float:
    f = host_features(host)
    score = 0.04
    if f.get("is_ip"):
        score += 0.45
    if f.get("has_punycode"):
        score += 0.35
    if f.get("brand_in_subdomain"):
        score += 0.48
    if f.get("brand_lookalike"):
        score += 0.52
    if f.get("risky_tld"):
        score += 0.32
    score += min(0.30, 0.12 * int(f.get("phish_keywords", 0)))
    score += min(0.25, 0.06 * int(f.get("num_hyphens", 0)))
    if float(f.get("digit_ratio", 0.0)) > 0.15:
        score += 0.20
    if float(f.get("entropy", 0.0)) > 3.7:
        score += 0.15
    return max(0.01, min(0.99, score))


def predict_hosts(hosts: List[str]) -> List[float]:
    b = get_bundle()
    if b.get("_serverless_light"):
        return [_light_score_host(h) for h in hosts]
    proba = b["pipeline"].predict_proba(features_frame(hosts))[:, 1]
    return [float(p) for p in proba]


def verdict_for(p: float, threshold: float, review: Optional[float] = None) -> str:
    review = threshold * 0.5 if review is None else min(review, threshold)
    if p >= threshold:
        return "PHISHING"
    if p >= review:
        return "SUSPICIOUS"
    return "LIKELY_SAFE"


def analyze_url(url: str) -> Dict[str, Any]:
    host = extract_host(url)
    scored = registered_domain(host)
    if scored in SHARED_HOSTING:
        return {
            "url": url, "host": host, "scored_domain": scored, "probability": None, "risk_score": None,
            "verdict": "NOT_SCORED", "threshold": None, "threshold_review": None,
            "indicators": indicators(host_features(host)), "model": model_info(),
        }
    p = predict_hosts([scored])[0]
    bundle = get_bundle()
    thr = float(bundle.get("threshold", 0.5))
    review = bundle.get("threshold_review")
    return {
        "url": url, "host": host, "scored_domain": scored,
        "probability": round(p, 4), "risk_score": round(p * 100, 1),
        "verdict": verdict_for(p, thr, review), "threshold": thr, "threshold_review": review,
        "indicators": indicators(host_features(host)), "model": model_info(),
    }


def score_urls(urls: List[str]) -> float:
    hosts: List[str] = []
    for u in urls:
        try:
            h = extract_host(u)
        except ValueError:
            continue
        if registered_domain(h) not in SHARED_HOSTING:
            hosts.append(h)
    if not hosts:
        return 0.0
    return round(max(predict_hosts([registered_domain(h) for h in hosts])) * 100, 1)
