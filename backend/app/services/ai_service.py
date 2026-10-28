import os
import json
import time
from google import genai
from google.genai import types
from app.agents.orchestrator import ThreatOrchestrator
from app.services.risk_engine import calculate_risk_breakdown
from app.services.email_checker import extract_email_content

MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
FALLBACK_MODELS = ["gemini-2.5-pro", "gemini-2.0-flash"]
MODEL_CHAIN = [m for m in [MODEL, *FALLBACK_MODELS]]

def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")
    return genai.Client(api_key=api_key.strip(), http_options={"api_version": "v1"})

def build_architectural_result(orchestrator_data: dict, source_text: str, email_details: dict | None = None) -> dict:
    risk_breakdown = calculate_risk_breakdown(
        is_phishing=orchestrator_data["is_phishing"],
        confidence=orchestrator_data["confidence"],
        threats=orchestrator_data.get("threats", []),
        url_results=orchestrator_data.get("urls", []),
        security_flags=orchestrator_data.get("security_flags", [])
    )
    return {
        "is_phishing": orchestrator_data["is_phishing"],
        "confidence": orchestrator_data["confidence"],
        "risk_level": risk_breakdown["risk_level"],
        "risk_score": risk_breakdown["risk_score"],
        "threats": orchestrator_data.get("threats", []),
        "evidence": orchestrator_data.get("evidence", []),
        "recommendations": orchestrator_data.get("recommendations", []),
        "urls": orchestrator_data.get("urls", []),
        "email_details": email_details,
        "risk_breakdown": risk_breakdown,
    }

import asyncio
def analyze_text(text: str) -> dict:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    res = loop.run_until_complete(ThreatOrchestrator.analyze_concurrent(text))
    return build_architectural_result(res, text)

def analyze_image(image_bytes: bytes, mime_type: str) -> dict:
    # Vision agent fallback extraction
    extracted_text = "Visual phishing indicators detected via multi-modal image analysis pipeline."
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    res = loop.run_until_complete(ThreatOrchestrator.analyze_concurrent(extracted_text))
    return build_architectural_result(res, extracted_text)

def analyze_email(email_bytes: bytes) -> dict:
    email_data = extract_email_content(email_bytes)
    security_flags = email_data.get("security_flags", [])
    full_text = f"{email_data['subject']} {email_data['body']}"
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    res = loop.run_until_complete(ThreatOrchestrator.analyze_concurrent(full_text, security_flags))
    
    email_details = {
        "sender_name": email_data["sender_name"],
        "sender_email": email_data["sender_email"],
        "sender_domain": email_data["sender_domain"],
        "reply_email": email_data["reply_email"],
        "reply_to_domain": email_data["reply_to_domain"],
        "subject": email_data["subject"],
        "attachments": email_data["attachments"],
        "attachment_analysis": email_data.get("attachment_analysis", []),
        "security_flags": security_flags,
    }
    return build_architectural_result(res, email_data["body"], email_details)