"""The privacy gateway. One path leads to a provider and it runs, in order:

  detect -> tokenize -> seal mapping (AES-256-GCM) -> split key (Shamir 2-of-3) -> forget key
  -> outbound leak check (fail closed) -> provider -> validate output -> store tokenized answer

Original values are restored only by `restore()`, and only after two valid shares open the vault.
"""
from __future__ import annotations

import hashlib
import re
import secrets
import threading
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Set

from . import vault
from .detector import detect, tokenize
from .provider import SYSTEM_PROMPT, Provider, ProviderPayload, ProviderUnavailable, describe
from .shamir import Share, ShareError, combine, decode_share, split
from .validation import ProviderOutputError, validate

TTL_SECONDS = 900
MAX_SESSIONS = 500
MAX_RESTORE_FAILURES = 5
MAX_TEXT = 8000
THRESHOLD, TOTAL = 2, 3
HOLDERS = ["A", "B", "C"]
_URL = re.compile(r"https?://[^\s<>\"')\]]+", re.IGNORECASE)
_TOKEN = re.compile(r"\[\[[A-Za-z_]+_\d+_[a-z0-9]{4}\]\]")


class GatewayBlocked(RuntimeError):
    """The gateway refused to contact the provider (fail closed)."""


class RestoreDenied(RuntimeError):
    """Restoration was refused. The message is safe to show to the caller."""


class SessionNotFound(KeyError):
    pass


@dataclass
class _Session:
    request_id: str
    kid: str
    nonce: bytes
    ciphertext: bytes
    issued_tokens: Set[str]
    expires: float
    tokenized_result: Optional[Dict[str, Any]] = None
    failures: int = 0


_sessions: Dict[str, _Session] = {}
_lock = threading.Lock()


def _purge(now: float) -> None:
    for rid in [r for r, s in _sessions.items() if s.expires < now]:
        del _sessions[rid]
    while len(_sessions) > MAX_SESSIONS:
        del _sessions[min(_sessions, key=lambda r: _sessions[r].expires)]


def reset_sessions() -> None:
    with _lock:
        _sessions.clear()


def drop_session(request_id: str) -> None:
    with _lock:
        _sessions.pop(request_id, None)


def assert_clean(payload: ProviderPayload, forbidden: Sequence[str]) -> int:
    """Raise GatewayBlocked if any forbidden string is present. Returns how many were checked."""
    haystack = payload.as_text()
    checked = 0
    for item in forbidden:
        if not item:
            continue
        checked += 1
        if item in haystack:
            raise GatewayBlocked("An original sensitive value or key material reached the outbound payload.")
    return checked


def _local_findings(text: str) -> Dict[str, Any]:
    """Runs on the ORIGINAL text, on this server only. Nothing here goes to the provider."""
    try:
        from app.real_detector.model import ModelNotAvailable, analyze_url
    except Exception:  # noqa: BLE001
        return {"status": "unavailable", "risk_score": 0, "urls": []}
    urls: List[Dict[str, Any]] = []
    seen: Set[str] = set()
    for match in _URL.finditer(text):
        url = match.group(0).rstrip(".,;:!?")
        if url in seen:
            continue
        seen.add(url)
        try:
            r = analyze_url(url)
        except ModelNotAvailable:
            return {"status": "model_missing", "risk_score": 0, "urls": []}
        except ValueError:
            continue
        urls.append({"url": url, "host": r["host"], "scored_domain": r["scored_domain"],
                     "verdict": r["verdict"], "risk_score": r["risk_score"]})
    scored = [u["risk_score"] for u in urls if u["risk_score"] is not None]
    return {"status": "ok", "risk_score": max(scored) if scored else 0, "urls": urls}


def _level(score: float) -> str:
    return "HIGH" if score >= 70 else "MEDIUM" if score >= 40 else "LOW"


def analyze(text: str, provider: Provider, protected_terms: Sequence[str] = ()) -> Dict[str, Any]:
    text = (text or "").strip()
    if not text:
        raise ValueError("Text is required.")
    if len(text) > MAX_TEXT:
        raise ValueError(f"Text is too long (maximum {MAX_TEXT} characters).")

    request_id = secrets.token_hex(8)
    spans = detect(text, protected_terms)
    sanitized, mapping, records = tokenize(text, spans)

    key = vault.new_key()
    nonce, ciphertext, kid = vault.seal(key, mapping, request_id)
    shares = split(key, THRESHOLD, TOTAL)
    encoded_shares = [s.encode() for s in shares]
    key_hex = key.hex()
    del key  # the gateway keeps no copy of the key: only the shares exist from here on

    payload = ProviderPayload(system=SYSTEM_PROMPT, sanitized_text=sanitized)
    forbidden = [*mapping.values(), *encoded_shares, key_hex, *(f"{s.y:x}" for s in shares)]
    checked = assert_clean(payload, forbidden)  # raises GatewayBlocked -> the provider is never called

    local = _local_findings(text)

    analysis: Optional[Dict[str, Any]] = None
    provider_status: Dict[str, Any] = {"status": "ok", "detail": None}
    try:
        validated = validate(provider.analyze(payload), set(mapping))
        analysis = validated.as_dict()
    except ProviderUnavailable as exc:
        provider_status = {"status": "unavailable", "detail": str(exc)}
    except ProviderOutputError as exc:
        provider_status = {"status": "invalid_output", "detail": str(exc)}

    now = time.time()
    with _lock:
        _purge(now)
        _sessions[request_id] = _Session(
            request_id=request_id, kid=kid, nonce=nonce, ciphertext=ciphertext,
            issued_tokens=set(mapping), expires=now + TTL_SECONDS, tokenized_result=analysis,
        )

    local_score = float(local["risk_score"])
    model_score = float(analysis["risk_score"]) if analysis else None
    if model_score is not None and model_score >= local_score:
        overall = {"risk_score": model_score, "source": provider.name}
    else:
        overall = {"risk_score": local_score, "source": "local detector"}
    overall["level"] = _level(overall["risk_score"])

    by_type: Dict[str, int] = {}
    for rec in records:
        by_type[rec["type"]] = by_type.get(rec["type"], 0) + 1

    return {
        "request_id": request_id,
        "expires_in": TTL_SECONDS,
        "provider": {**describe(provider), **provider_status},
        "detection": {"count": len(records), "by_type": by_type, "spans": records},
        "sanitized_text": sanitized,
        "outbound": {
            "fields": ["system", "sanitized_text"],
            "bytes": len(payload.as_text().encode("utf-8")),
            "sha256": hashlib.sha256(payload.as_text().encode("utf-8")).hexdigest(),
            "forbidden_strings_checked": checked,
            "leak_check": "passed",
        },
        "vault": {"cipher": "AES-256-GCM", "nonce_bits": 96, "kid": kid,
                  "ciphertext_bytes": len(ciphertext), "bound_to": "request id + key id"},
        "custody": {
            "scheme": "Shamir over GF(2^521 - 1)", "threshold": THRESHOLD, "total": TOTAL, "kid": kid,
            "shares": [{"holder": h, "share": s} for h, s in zip(HOLDERS, encoded_shares)],
            "note": "Demo mode: all three shares are shown here. In real use each goes to a different holder.",
        },
        "analysis": analysis,
        "local": local,
        "overall": overall,
    }


def _restore_text(text: str, mapping: Dict[str, str]) -> str:
    return _TOKEN.sub(lambda m: mapping.get(m.group(0), m.group(0)), text)


def restore(request_id: str, share_texts: Sequence[str]) -> Dict[str, Any]:
    """Open the vault with the given shares and restore values in the stored answer."""
    with _lock:
        _purge(time.time())
        session = _sessions.get(request_id)
        if session is None:
            raise SessionNotFound(request_id)
        if session.failures >= MAX_RESTORE_FAILURES:
            del _sessions[request_id]
            raise RestoreDenied("Too many failed attempts. This vault has been destroyed.")

    def fail(message: str) -> RestoreDenied:
        with _lock:
            s = _sessions.get(request_id)
            if s is not None:
                s.failures += 1
        return RestoreDenied(message)

    try:
        shares: List[Share] = [decode_share(t) for t in share_texts]
    except ShareError as exc:
        raise fail(str(exc)) from None
    if any(s.kid != session.kid for s in shares):
        raise fail("A share belongs to a different request.")
    try:
        key = combine(shares, THRESHOLD)
    except ShareError as exc:
        raise fail(str(exc)) from None
    try:
        mapping = vault.open_vault(key, session.nonce, session.ciphertext, request_id, session.kid)
    except vault.VaultError:
        raise fail("These shares do not open the vault.") from None

    result = session.tokenized_result
    if result is None:
        raise RestoreDenied("There is no provider answer to restore for this request.")
    # Restoration is limited to tokens this request issued; provider output cannot widen it.
    allowed = {t: v for t, v in mapping.items() if t in session.issued_tokens}
    return {
        "restored": True,
        "values_restored": len(allowed),
        "reasons": [_restore_text(r, allowed) for r in result["reasons"]],
        "recommendations": [_restore_text(r, allowed) for r in result["recommendations"]],
    }
