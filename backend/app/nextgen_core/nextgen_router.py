from pathlib import Path
from typing import List, Dict, Any
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from app.nextgen_core.quad_architecture_master import SovereignUnifiedQuadArchitecture

router = APIRouter(prefix="/api/v1/nextgen", tags=["Next-Gen Quad-Core Architecture"])


class QuadAnalyzeRequest(BaseModel):
    message_text: str = Field(..., description="نص الرسالة المراد تحليلها")
    extracted_urls: List[str] = Field(default_factory=list)
    url_risk_score: float = Field(default=88.0)
    prior_thread_topic: str = Field(default="GENERAL_OPERATIONS")
    sender_verified_role: str = Field(default="EXTERNAL_UNVERIFIED")
    research_advisory_text: str = Field(default="")


@router.get("/dashboard", response_class=HTMLResponse)
def serve_nextgen_quad_dashboard() -> HTMLResponse:
    html_path = Path(__file__).resolve().parent / "nextgen_dashboard.html"
    return HTMLResponse(content=html_path.read_text(encoding="utf-8"), status_code=200)


@router.post("/analyze")
def execute_nextgen_quad_pipeline(req: QuadAnalyzeRequest) -> Dict[str, Any]:
    return SovereignUnifiedQuadArchitecture.execute_quad_architecture(
        message_text=req.message_text,
        extracted_urls=req.extracted_urls,
        url_risk_score=req.url_risk_score,
        prior_thread_topic=req.prior_thread_topic,
        sender_verified_role=req.sender_verified_role,
        research_advisory_text=req.research_advisory_text
    )