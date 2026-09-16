import json
import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types

try:
    from app.services.email_checker import extract_email_content
    from app.services.url_checker import extract_urls, analyze_url
    from app.services.risk_engine import calculate_risk_breakdown
except ImportError:
    from services.email_checker import extract_email_content
    from services.url_checker import extract_urls, analyze_url
    from services.risk_engine import calculate_risk_breakdown

load_dotenv()

MODEL = "gemini-2.0-flash"


def get_gemini_client():
    """
    Lazy initialization of the Gemini client to avoid import-time crashes.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured in Environment Variables.")
    return genai.Client(api_key=api_key.strip())


def generate_ai_response(contents) -> str:
    """
    Call Gemini with retry support for temporary errors.
    """
    client = get_gemini_client()
    last_error = None

    for attempt in range(2):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=contents,
            )

            if not response.text:
                raise RuntimeError("Gemini returned an empty response.")

            return response.text

        except Exception as exc:
            last_error = exc
            error_text = str(exc)

            if "503" in error_text or "UNAVAILABLE" in error_text or "RESOURCE_EXHAUSTED" in error_text:
                time.sleep(1)
                continue

            raise

    raise RuntimeError(f"Gemini service unavailable after retries: {last_error}")


def parse_ai_response(response_text: str) -> dict:
    """
    Convert Gemini JSON response into a Python dictionary.
    """
    result = response_text.strip()

    if result.startswith("```"):
        result = (
            result.replace("```json", "", 1)
            .replace("```", "")
            .strip()
        )

    try:
        return json.loads(result)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Gemini returned invalid JSON: {result}") from exc


def normalize_text(value: str) -> str:
    """
    Normalize text for duplicate detection.
    """
    return " ".join(value.lower().strip().split())


def run_heuristic_fallback(source_text: str, security_flags: list[str] | None = None) -> dict:
    """
    Deterministic security analysis fallback engine.
    Executes when Gemini API is rate-limited, unreachable, or returns 503.
    """
    security_flags = security_flags or []
    threats = []
    evidence = list(security_flags)
    text_lower = source_text.lower()

    # 1. Suspicious keywords heuristics
    urgent_terms = ["urgent", "immediately", "account suspended", "verify your identity", "password reset", "unauthorized login", "action required"]
    detected_urgency = [term for term in urgent_terms if term in text_lower]
    if detected_urgency:
        threats.append("Social Engineering")
        evidence.append(f"Artificial urgency patterns detected: {', '.join(detected_urgency)}")

    credential_terms = ["password", "verify password", "ssn", "credit card", "billing update"]
    detected_creds = [term for term in credential_terms if term in text_lower]
    if detected_creds:
        threats.append("Credential Theft")
        evidence.append("Message directly references sensitive credentials or verification.")

    # 2. Analyze URLs deterministically
    urls = extract_urls(source_text)
    high_risk_urls = 0

    for u in urls:
        analysis = analyze_url(u)
        if analysis.get("risk_score", 0) >= 50:
            high_risk_urls += 1
            evidence.extend(analysis.get("reasons", []))

    if high_risk_urls > 0:
        threats.append("Malicious Links")

    # 3. Incorporate deterministic email security flags
    for flag in security_flags:
        flag_lower = flag.lower()
        if "spoofing" in flag_lower or "impersonate" in flag_lower:
            if "Brand Impersonation" not in threats:
                threats.append("Brand Impersonation")
        if "reply-to" in flag_lower and "Reply-To Mismatch" not in threats:
            threats.append("Reply-To Mismatch")
        if "attachment" in flag_lower and "Malicious Attachments" not in threats:
            threats.append("Malicious Attachments")

    is_phishing = bool(threats or high_risk_urls > 0 or len(security_flags) > 0)
    confidence = 0.85 if is_phishing else 0.90

    if not threats:
        evidence.append("No obvious malicious triggers detected via heuristic analysis engine.")

    recommendations = [
        "Do not submit credentials or sensitive personal details.",
        "Verify communications directly via official provider portals.",
    ]
    if is_phishing:
        recommendations.insert(0, "Do not click links or execute attachments from this communication.")

    return {
        "is_phishing": is_phishing,
        "confidence": confidence,
        "threats": threats or ["Unverified Communication"],
        "evidence": list(set(evidence)),
        "recommendations": recommendations,
        "security_flags": security_flags,
    }


def build_final_result(
    data: dict,
    source_text: str,
    email_details: dict | None = None,
) -> dict:
    """
    Combine AI/Heuristic analysis, URL analysis, risk engine,
    and optional email metadata.
    """
    urls = extract_urls(source_text)
    url_results = [analyze_url(url) for url in urls]

    risk_breakdown = calculate_risk_breakdown(
        is_phishing=data["is_phishing"],
        confidence=data["confidence"],
        threats=data.get("threats", []),
        url_results=url_results,
        security_flags=data.get("security_flags", []),
    )

    risk_score = risk_breakdown["risk_score"]
    risk_level = risk_breakdown["risk_level"]

    unique_threats = []
    seen_threats = set()
    for threat in data.get("threats", []):
        key = normalize_text(threat)
        if key not in seen_threats:
            seen_threats.add(key)
            unique_threats.append(threat)

    unique_evidence = []
    seen_evidence = set()
    for item in data.get("evidence", []):
        key = normalize_text(item)
        if key not in seen_evidence:
            seen_evidence.add(key)
            unique_evidence.append(item)

    return {
        "is_phishing": data["is_phishing"],
        "confidence": data["confidence"],
        "risk_level": risk_level,
        "risk_score": risk_score,
        "threats": unique_threats,
        "evidence": unique_evidence,
        "recommendations": data.get("recommendations", []),
        "urls": url_results,
        "email_details": email_details,
        "risk_breakdown": risk_breakdown,
    }


def analyze_text(text: str) -> dict:
    """
    Analyze a text message with Gemini, falling back to heuristics on failure.
    """
    prompt = f"""
You are an expert cybersecurity threat analyst.

Analyze this message for:
- phishing
- scams
- social engineering
- credential theft
- impersonation
- financial fraud
- malicious links

Return ONLY valid JSON.
Do not use Markdown.
Do not add text before or after the JSON.

Use exactly this structure:
{{
  "is_phishing": true,
  "confidence": 0.99,
  "threats": ["Credential Theft"],
  "evidence": ["Requests password verification"],
  "recommendations": ["Do not provide credentials"]
}}

Rules:
- confidence must be between 0 and 1.
- Do not invent evidence.
- Only report evidence actually present in the message.
- Keep threats concise.
- Keep evidence specific.
- Give practical safety recommendations.

Message:
{text}
"""
    try:
        response_text = generate_ai_response(prompt)
        data = parse_ai_response(response_text)
    except Exception as exc:
        print(f"[FALLBACK ACTIVATED] Text Analysis fallback engaged. Error: {exc}")
        data = run_heuristic_fallback(source_text=text)

    return build_final_result(
        data=data,
        source_text=text,
    )

def analyze_image(
    image_bytes: bytes,
    mime_type: str,
) -> dict:
    """
    Analyze a screenshot directly with Gemini vision, with heuristic fallback.
    """
    prompt = """
You are an expert cybersecurity threat analyst.

Analyze this screenshot for:
- phishing
- scams
- social engineering
- credential theft
- impersonation
- financial fraud
- malicious links

Read the visible text carefully.

Return ONLY valid JSON.
Do not use Markdown.
Do not add text before or after the JSON.

Use exactly this structure:
{
  "is_phishing": true,
  "confidence": 0.99,
  "extracted_text": "Text visible in the screenshot",
  "threats": ["Credential Theft"],
  "evidence": ["Requests password verification"],
  "recommendations": ["Do not provide credentials"]
}

Rules:
- confidence must be between 0 and 1.
- extracted_text must contain only text actually visible in the screenshot.
- Do not invent evidence.
- Keep threats concise.
- Keep evidence specific.
- Give practical safety recommendations.
"""
    try:
        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type=mime_type,
        )
        response_text = generate_ai_response(contents=[prompt, image_part])
        data = parse_ai_response(response_text)
        extracted_text = data.get("extracted_text", "")
    except Exception as exc:
        print(f"[FALLBACK ACTIVATED] Image Analysis fallback engaged. Error: {exc}")
        extracted_text = "Image text extraction unavailable during offline fallback mode."
        data = run_heuristic_fallback(source_text=extracted_text)
        data["evidence"].append(f"Fallback triggered: {str(exc)[:80]}")

    return build_final_result(
        data=data,
        source_text=extracted_text,
    )

def analyze_email(email_bytes: bytes) -> dict:
    """
    Analyze an .eml email using deterministic parser + Gemini (with heuristic fallback).
    """
    email_data = extract_email_content(email_bytes)
    security_flags = email_data.get("security_flags", [])

    email_text = f"""
From: {email_data["from"]}
Sender name: {email_data["sender_name"]}
Sender email: {email_data["sender_email"]}
Sender domain: {email_data["sender_domain"]}

To: {email_data["to"]}

Reply-To: {email_data["reply_to"]}
Reply-To email: {email_data["reply_email"]}
Reply-To domain: {email_data["reply_to_domain"]}

Subject: {email_data["subject"]}

Attachments:
{email_data["attachments"]}

Attachment analysis:
{email_data.get("attachment_analysis", [])}

Deterministic security flags:
{security_flags}

Body:
{email_data["body"]}
"""

    prompt = f"""
You are an expert email security analyst.

Analyze this email for:
- phishing
- spoofing
- brand impersonation
- credential theft
- social engineering
- financial fraud
- malicious links
- suspicious sender behavior
- Reply-To mismatches
- suspicious attachments
- display-name impersonation

The email parser has already performed deterministic checks.
Treat those checks as important evidence.

Return ONLY valid JSON.
Do not use Markdown.
Do not add text before or after the JSON.

Use exactly this structure:
{{
  "is_phishing": true,
  "confidence": 0.99,
  "threats": ["Brand Impersonation", "Reply-To Mismatch"],
  "evidence": ["The sender domain is suspicious."],
  "recommendations": ["Do not click links or open attachments."]
}}

Rules:
- confidence must be between 0 and 1.
- Do not invent facts.
- Only use evidence present in the email.
- Mention relevant deterministic security flags.

Email:
{email_text}
"""
    try:
        response_text = generate_ai_response(prompt)
        data = parse_ai_response(response_text)
    except Exception as exc:
        print(f"[FALLBACK ACTIVATED] Email Analysis fallback engaged. Error: {exc}")
        data = run_heuristic_fallback(
            source_text=f"{email_data['subject']} {email_data['body']}",
            security_flags=security_flags,
        )

    # Preserve deterministic findings
    data["security_flags"] = security_flags

    # Add deterministic evidence without duplicates
    existing_evidence = {normalize_text(item) for item in data.get("evidence", [])}
    for flag in security_flags:
        norm_flag = normalize_text(flag)
        if norm_flag not in existing_evidence:
            data.setdefault("evidence", []).append(flag)
            existing_evidence.add(norm_flag)

    # Add Reply-To mismatch threat if present
    existing_threats = {normalize_text(item) for item in data.get("threats", [])}
    if (
        "Reply-To address does not match the From address." in security_flags
        and "reply-to mismatch" not in existing_threats
    ):
        data.setdefault("threats", []).append("Reply-To Mismatch")

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

    return build_final_result(
        data=data,
        source_text=email_data["body"],
        email_details=email_details,
    )