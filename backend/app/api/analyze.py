from fastapi import APIRouter
from app.schemas import AnalyzeRequest, AnalyzeResponse
from app.services.ai_service import analyze_text

router = APIRouter(
    prefix="/analyze",
    tags=["Analyze"]
)


@router.post("/", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    return analyze_text(request.text)