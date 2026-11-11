"""Model loading + inference. The score comes ONLY from the trained model."""
from __future__ import annotations

import logging
import os
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional

import joblib

from .features import SHARED_HOSTING, extract_host, features_frame, host_features, indicators, registered_domain

log = logging.getLogger("phishguard.detector")

# backend/app/real_detector/model.py -> parents[2] == backend/
DEFAULT_MODEL_PATH = Path(__file__).resolve().parents[2] / "models" / "url_model.joblib"

_lock = threading.Lock()
_bundle: Optional[Dict[str, Any]] = None


class ModelNotAvailable(RuntimeError):
    """Raised when no usable trained model can be loaded."""


def model_path() -> Path:
    return Path(os.environ.get("PHISHGUARD_MODEL", str(DEFAULT_MODEL_PATH)))


def set_bundle(bundle: Optional[Dict[str, Any]]) -> None:
    """Inject (or clear) the model bundle. Used by tests and by training."""
    global _bundle
    with _lock:
        _bundle = bundle


def get_bundle() -> Dict[str, Any]:
    global _bundle
    with _lock:
        if _bundle is not None:
            return _bundle
        path = model_path()
        if not path.exists():
            raise ModelNotAvailable(
                f"No trained model at {path}. Run: python scripts/fetch_data.py && python scripts/train.py"
            )
        try:
            _bundle = joblib.load(path)
        except Exception as exc:  # version mismatch, corrupted file...
            raise ModelNotAvailable(
                f"Could not load model ({exc.__class__.__name__}). Retrain with: python scripts/train.py"
            ) from exc
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


def predict_hosts(hosts: List[str]) -> List[float]:
    b = get_bundle()
    proba = b["pipeline"].predict_proba(features_frame(hosts))[:, 1]
    return [float(p) for p in proba]


def verdict_for(p: float, threshold: float, review: Optional[float] = None) -> str:
    """>= block threshold -> PHISHING, >= review threshold -> SUSPICIOUS, else LIKELY_SAFE."""
    review = threshold * 0.5 if review is None else min(review, threshold)
    if p >= threshold:
        return "PHISHING"
    if p >= review:
        return "SUSPICIOUS"
    return "LIKELY_SAFE"


def analyze_url(url: str) -> Dict[str, Any]:
    host = extract_host(url)  # ValueError -> caller turns into HTTP 422
    scored = registered_domain(host)
    if scored in SHARED_HOSTING:
        # the platform's domain says nothing about one site hosted on it -> refuse to give a score
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
        "url": url,
        "host": host,
        "scored_domain": scored,
        "probability": round(p, 4),
        "risk_score": round(p * 100, 1),
        "verdict": verdict_for(p, thr, review),
        "threshold": thr,
        "threshold_review": review,
        "indicators": indicators(host_features(host)),
        "model": model_info(),
    }


def score_urls(urls: List[str]) -> float:
    """Max risk score (0-100) over the usable URLs. 0.0 when there are none."""
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
