from typing import List

from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    text: str


class URLAnalysis(BaseModel):
    url: str
    hostname: str
    risk_score: int
    risk_level: str
    reasons: List[str]


class AttachmentAnalysis(BaseModel):
    filename: str
    risk_score: int
    risk_level: str
    reasons: List[str]


class EmailDetails(BaseModel):
    sender_name: str
    sender_email: str
    sender_domain: str
    reply_email: str
    reply_to_domain: str
    subject: str
    attachments: List[str]
    attachment_analysis: List[AttachmentAnalysis]
    security_flags: List[str]


class RiskContribution(BaseModel):
    signal: str
    source: str
    points: float


class RiskBreakdown(BaseModel):
    raw_score: float
    risk_score: int
    risk_level: str
    capped: bool
    highest_url_score: int
    contributions: List[RiskContribution]


class AnalyzeResponse(BaseModel):
    is_phishing: bool
    confidence: float
    risk_level: str
    risk_score: int
    threats: List[str]
    evidence: List[str]
    recommendations: List[str]
    urls: List[URLAnalysis]
    email_details: EmailDetails | None = None
    risk_breakdown: RiskBreakdown | None = None