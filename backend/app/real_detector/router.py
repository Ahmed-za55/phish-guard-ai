from __future__ import annotations
from pathlib import Path
from typing import Any, Dict

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from . import model as detector

router = APIRouter(prefix="/api/v1/detect", tags=["Real URL detector"])


class DetectRequest(BaseModel):
    url: str = Field(..., min_length=1, max_length=2048, description="URL or hostname to check")


@router.post("")
def detect(req: DetectRequest) -> Dict[str, Any]:
    try:
        return detector.analyze_url(req.url)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=f"Unusable URL: {exc}")
    except detector.ModelNotAvailable as exc:
        raise HTTPException(status_code=503, detail=str(exc))


@router.get("/health")
def health() -> Dict[str, Any]:
    try:
        return {"status": "ok", "model": detector.model_info()}
    except detector.ModelNotAvailable as exc:
        return {"status": "model_missing", "detail": str(exc)}


@router.get("/ui", response_class=HTMLResponse)
def ui() -> HTMLResponse:
    html = (Path(__file__).resolve().parent / "ui.html").read_text(encoding="utf-8")
    return HTMLResponse(content=html)
