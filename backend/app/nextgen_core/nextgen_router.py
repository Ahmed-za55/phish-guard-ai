from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Any, Optional
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from app.nextgen_core.quad_architecture_master import SovereignUnifiedQuadArchitecture

router = APIRouter(prefix="/api/v1/nextgen", tags=["Next-Gen Quad-Core Architecture"])


class QuadAnalyzeRequest(BaseModel):
    message_text: str = Field(..., description="نص الرسالة المراد تحليلها")
    extracted_urls: List[str] = Field(default_factory=list)
    url_risk_score: Optional[float] = Field(default=None, description="Ignored: computed server-side by the trained URL detector")
    prior_thread_topic: str = Field(default="GENERAL_OPERATIONS")
    sender_verified_role: str = Field(default="EXTERNAL_UNVERIFIED")
    research_advisory_text: str = Field(default="")


@router.get("/dashboard", response_class=HTMLResponse)
def serve_nextgen_quad_dashboard() -> HTMLResponse:
    html_path = Path(__file__).resolve().parent / "nextgen_dashboard.html"
    return HTMLResponse(content=html_path.read_text(encoding="utf-8"), status_code=200)


def _resolve_url_risk(req) -> float:
    """URL risk is ALWAYS computed server-side by the trained detector.
    Any url_risk_score sent by a client is ignored (kept in the schema only for old clients)."""
    from fastapi import HTTPException
    from app.real_detector.model import ModelNotAvailable, score_urls
    try:
        return score_urls(req.extracted_urls)
    except ModelNotAvailable as exc:
        raise HTTPException(status_code=503, detail=str(exc))


@router.post("/analyze")
def execute_nextgen_quad_pipeline(req: QuadAnalyzeRequest) -> Dict[str, Any]:
    return SovereignUnifiedQuadArchitecture.execute_quad_architecture(
        message_text=req.message_text,
        extracted_urls=req.extracted_urls,
        url_risk_score=_resolve_url_risk(req),
        prior_thread_topic=req.prior_thread_topic,
        sender_verified_role=req.sender_verified_role,
        research_advisory_text=req.research_advisory_text
    )
