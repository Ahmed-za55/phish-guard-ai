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
    inds = indicators(f)
    score = 0.03
    # Weight each triggered domain indicator from features.py
    score += 0.26 * len(inds)
    for k, w in (
        ("is_ip", 0.45),
        ("has_punycode", 0.40),
        ("brand_in_subdomain", 0.45),
        ("brand_in_domain", 0.38),
        ("brand_lookalike", 0.48),
        ("risky_tld", 0.30),
        ("suspicious_tld", 0.30),
    ):
        if f.get(k):
            score += w
    h_lower = host.lower()
    brands = ("paypal", "apple", "google", "microsoft", "amazon", "netflix", "bank", "chase", "wellsfargo", "binance", "coinbase", "metamask")
    kw_hits = sum(1 for kw in ("secure", "login", "verify", "update", "account", "confirm", "signin", "wallet", "auth", "support", "alert") if kw in h_lower)
    brand_hits = sum(1 for b in brands if b in h_lower and not h_lower.endswith(f"{b}.com"))
    score += min(0.45, 0.22 * kw_hits)
    score += min(0.45, 0.35 * brand_hits)
    hyphen_count = h_lower.count("-")
    if hyphen_count >= 2:
        score += min(0.30, 0.10 * hyphen_count)
    digits = sum(c.isdigit() for c in h_lower)
    if digits >= 3:
        score += 0.22
    return max(0.02, min(0.98, score))


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
    p = _light_score_host(host) if get_bundle().get('_serverless_light') else predict_hosts([scored])[0]
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
