from __future__ import annotations
import threading
import time
from collections import defaultdict, deque
from typing import Any, Deque, Dict, List

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from . import selftest, service
from .provider import default_provider

router = APIRouter(prefix="/api/v1/private", tags=["Private analysis"])

_WINDOW_SECONDS, _MAX_CALLS = 60, 20
_calls: Dict[str, Deque[float]] = defaultdict(deque)
_calls_lock = threading.Lock()


def _rate_limit(request: Request) -> None:
    ip = request.client.host if request.client else "unknown"
    now = time.time()
    with _calls_lock:
        window = _calls[ip]
        while window and now - window[0] > _WINDOW_SECONDS:
            window.popleft()
        if len(window) >= _MAX_CALLS:
            raise HTTPException(status_code=429, detail="Too many requests. Wait a minute and try again.")
        window.append(now)


class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=service.MAX_TEXT)
    protected_terms: List[str] = Field(default_factory=list, max_length=20)


class RestoreRequest(BaseModel):
    request_id: str = Field(..., min_length=4, max_length=64)
    shares: List[str] = Field(..., min_length=1, max_length=3)


@router.post("/analyze")
def analyze(body: AnalyzeRequest, request: Request) -> Dict[str, Any]:
    _rate_limit(request)
    terms = [t[:80] for t in body.protected_terms]
    try:
        return service.analyze(body.text, default_provider(), terms)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    except service.GatewayBlocked:
        # Fail closed: nothing was sent to any provider.
        raise HTTPException(status_code=500, detail="The privacy gateway blocked this request. Nothing was sent.")


@router.post("/restore")
def restore(body: RestoreRequest, request: Request) -> Dict[str, Any]:
    _rate_limit(request)
    try:
        return service.restore(body.request_id, body.shares)
    except service.SessionNotFound:
        raise HTTPException(status_code=404, detail="This request has expired or does not exist.")
    except service.RestoreDenied as exc:
        raise HTTPException(status_code=403, detail=str(exc))


@router.get("/selftest")
def run_selftest(request: Request) -> Dict[str, Any]:
    _rate_limit(request)
    return selftest.run()


@router.get("/status")
def status() -> Dict[str, Any]:
    provider = default_provider()
    return {"provider": provider.name, "model": getattr(provider, "model", None),
            "cipher": "AES-256-GCM", "threshold": service.THRESHOLD, "total": service.TOTAL}
