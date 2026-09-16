import os
import sys
from pathlib import Path

# إعداد مسارات بايثون لدعم بيئة سيرفرات Vercel
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR.parent) not in sys.path:
    sys.path.insert(0, str(BASE_DIR.parent))
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

try:
    from app.schemas import AnalyzeRequest, AnalyzeResponse
    from app.services.ai_service import analyze_text, analyze_image, analyze_email
    from app.rate_limit import RateLimiter
except ImportError:
    from schemas import AnalyzeRequest, AnalyzeResponse
    from services.ai_service import analyze_text, analyze_image, analyze_email
    from rate_limit import RateLimiter


MAX_TEXT_LENGTH = int(os.getenv("MAX_TEXT_LENGTH", "20000"))
MAX_IMAGE_SIZE = int(os.getenv("MAX_IMAGE_SIZE", str(10 * 1024 * 1024)))
MAX_EMAIL_SIZE = int(os.getenv("MAX_EMAIL_SIZE", str(10 * 1024 * 1024)))

# Rate limiting
RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "10"))
RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", "60"))

rate_limiter = RateLimiter(
    max_requests=RATE_LIMIT_REQUESTS,
    window_seconds=RATE_LIMIT_WINDOW,
)

app = FastAPI(
    title="Phish Guard AI",
    version="1.0.0",
    description="AI-powered phishing and scam detection platform.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def safe_error(message: str, status_code: int = 500) -> HTTPException:
    return HTTPException(status_code=status_code, detail=message)


def check_rate_limit(request: Request) -> None:
    allowed, retry_after = rate_limiter.allow(request)
    if not allowed:
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please try again later.",
            headers={"Retry-After": str(retry_after)},
        )


@app.get("/")
@app.get("/api/backend/")
def root():
    return {"project": "Phish Guard AI", "status": "running"}


@app.get("/health")
@app.get("/api/backend/health")
def health():
    return {"ok": True}


@app.post("/analyze", response_model=AnalyzeResponse)
@app.post("/api/backend/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest, http_request: Request):
    check_rate_limit(http_request)

    if not request.text or not request.text.strip():
        raise safe_error("Text content is required.", 400)

    text = request.text.strip()
    if len(text) > MAX_TEXT_LENGTH:
        raise safe_error(
            f"Text is too long. Maximum length is {MAX_TEXT_LENGTH} characters.",
            413,
        )

    try:
        return analyze_text(text)
    except HTTPException:
        raise
    except Exception:
        raise safe_error("Text analysis is temporarily unavailable.", 503)


@app.post("/analyze-image", response_model=AnalyzeResponse)
@app.post("/api/backend/analyze-image", response_model=AnalyzeResponse)
async def analyze_image_endpoint(request: Request, file: UploadFile = File(...)):
    check_rate_limit(request)

    allowed_types = {"image/jpeg", "image/png", "image/webp"}

    try:
        if not file.filename:
            raise safe_error("No image file provided.", 400)

        if file.content_type not in allowed_types:
            raise safe_error("Unsupported image type. Use JPEG, PNG, or WEBP.", 400)

        image_bytes = await file.read()
        if not image_bytes:
            raise safe_error("Image file is empty.", 400)

        if len(image_bytes) > MAX_IMAGE_SIZE:
            raise safe_error("Image file is too large.", 413)

        return analyze_image(image_bytes=image_bytes, mime_type=file.content_type)
    except HTTPException:
        raise
    except Exception:
        raise safe_error("Image analysis is temporarily unavailable.", 503)


@app.post("/analyze-email", response_model=AnalyzeResponse)
@app.post("/api/backend/analyze-email", response_model=AnalyzeResponse)
async def analyze_email_endpoint(request: Request, file: UploadFile = File(...)):
    check_rate_limit(request)

    try:
        if not file.filename:
            raise safe_error("No email file provided.", 400)

        if not file.filename.lower().endswith(".eml"):
            raise safe_error("Only .eml files are supported.", 400)

        email_bytes = await file.read()
        if not email_bytes:
            raise safe_error("The email file is empty.", 400)

        if len(email_bytes) > MAX_EMAIL_SIZE:
            raise safe_error("Email file is too large.", 413)

        return analyze_email(email_bytes)
    except HTTPException:
        raise
    except Exception:
        raise safe_error("Email analysis is temporarily unavailable.", 503)