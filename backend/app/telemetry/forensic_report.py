import uuid
from datetime import datetime
from typing import Dict, Any

class ForensicReportGenerator:
    """
    Generates standardized threat intelligence forensic reports (STIX-inspired format) 
    for enterprise security operations centers (SOC).
    """
    @staticmethod
    def generate_report(analysis_result: Dict[str, Any], payload_snippet: str) -> Dict[str, Any]:
        report_id = f"report--{uuid.uuid4()}"
        timestamp = datetime.utcnow().isoformat() + "Z"

        return {
            "stix_version": "2.1",
            "id": report_id,
            "created": timestamp,
            "modified": timestamp,
            "name": "PhishGuard AI Autonomous Forensic Threat Assessment",
            "description": "Automated security analytics breakdown utilizing mathematical entropy, Levenshtein distance, and behavioral sandbox telemetry.",
            "threat_level": analysis_result.get("risk_level", "LOW"),
            "risk_score": analysis_result.get("risk_score", 0),
            "indicators": analysis_result.get("threats", []),
            "evidence_collection": analysis_result.get("evidence", []),
            "mitigation_recommendations": analysis_result.get("recommendations", []),
            "payload_fingerprint_snippet": payload_snippet[:120] + "..." if len(payload_snippet) > 120 else payload_snippet
        }