import json
from pathlib import Path
from typing import List, Dict, Any
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from app.infinity_dominion_v11.dominion_master import InfinityDominionPlatformV11

router = APIRouter(prefix="/api/v1/dominion", tags=["Infinity Dominion v11.0 (7-Plane Architecture)"])


class DominionAnalyzeRequest(BaseModel):
    text: str = Field(..., description="النص أو محتوى البريد المراد فحصه عبر المستويات السبعة")
    extracted_urls: List[str] = Field(default_factory=list, description="الروابط المستخرجة")
    url_results: List[Dict[str, Any]] = Field(default_factory=list, description="نتائج الفحص الأولي للروابط")
    entropy_val: float = Field(default=4.88, description="قيمة الإنتروبيا المحسوبة للنص")


class CrossPlaneCheckRequest(BaseModel):
    caller_identity: str
    target_plane: str
    requested_mode: str = "WRITE"


@router.get("/dashboard", response_class=HTMLResponse)
def serve_sovereign_7_plane_dashboard() -> HTMLResponse:
    """عرض واجهة لوحة التحكم التفاعلية للمستويات السبعة (Sovereign 7-Plane Command Dashboard)."""
    html_path = Path(__file__).resolve().parent / "dominion_dashboard.html"
    return HTMLResponse(content=html_path.read_text(encoding="utf-8"), status_code=200)


@router.post("/analyze")
def analyze_via_7_planes(req: DominionAnalyzeRequest) -> Dict[str, Any]:
    """تشغيل الفحص الكامل عبر المستويات السبعة المعزولة لإصدار Infinity Dominion v11.0."""
    return InfinityDominionPlatformV11.execute_distributed_7_plane_pipeline(
        text=req.text,
        extracted_urls=req.extracted_urls,
        url_results=req.url_results,
        entropy_val=req.entropy_val
    )


@router.post("/verify-boundary")
def verify_cross_plane_isolation(req: CrossPlaneCheckRequest) -> Dict[str, Any]:
    """اختبار حواجز العزل بين المستويات السبعة (Cross-Plane Zero-Trust Verification)."""
    return InfinityDominionPlatformV11.verify_cross_plane_boundary(
        caller_identity=req.caller_identity,
        target_plane=req.target_plane,
        requested_mode=req.requested_mode
    )


@router.get("/trifecta-status")
def get_trifecta_verification_status() -> Dict[str, Any]:
    """إرجاع نتائج التحقق الثلاثي للإصدار (OOD Generalization + Insider Containment + P95/P99 Benchmark)."""
    report_path = Path("E:/phish-guard-ai/backend/tests/infinity_dominion_v11_trifecta_report.json")
    if report_path.exists():
        return json.loads(report_path.read_text(encoding="utf-8"))
    return {
        "overall_status": "PENDING_TRIFECTA_RUN",
        "message": "Run test_infinity_dominion_trifecta.py to generate the live verification artifact."
    }