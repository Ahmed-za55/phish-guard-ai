from typing import Dict, Any, List
from app.services.url_checker import analyze_url, extract_urls
from app.storage.vector_cache import ThreatMemoryCache

class ThreatOrchestrator:
    """
    Architectural Orchestrator with Threat Memory Cache: Checks local cryptographic 
    fingerprints before dispatching to heuristic and mathematical security models.
    """
    @staticmethod
    async def analyze_concurrent(text: str, security_flags: List[str] = None) -> Dict[str, Any]:
        security_flags = security_flags or []
        
        # 1. Check Threat Intelligence Cache first for lightning-fast matching
        cached_result = ThreatMemoryCache.get(text)
        if cached_result:
            cached_result["cached_hit"] = True
            return cached_result

        urls = extract_urls(text)
        url_results = [analyze_url(u) for u in urls]
        evidence = list(security_flags)
        threats = []
        
        for u_res in url_results:
            if u_res["risk_score"] >= 45:
                threats.append("Malicious Links")
                evidence.extend(u_res["reasons"])

        text_lower = text.lower()
        if any(term in text_lower for term in ["urgent", "verify", "suspended", "immediate"]):
            threats.append("Social Engineering")
            evidence.append("High-urgency social engineering linguistic patterns detected.")

        if any("Levenshtein" in r or "impersonat" in r for u_res in url_results for r in u_res["reasons"]):
            threats.append("Brand Impersonation")

        is_phishing = bool(threats or len(url_results) > 0 or len(security_flags) > 0)
        confidence = 0.95 if is_phishing else 0.92

        result = {
            "is_phishing": is_phishing,
            "confidence": confidence,
            "threats": list(set(threats)) or ["Unverified Communication"],
            "evidence": list(set(evidence)),
            "recommendations": [
                "Do not submit credentials, banking info, or personal verification data.",
                "Verify communications independently through official application channels."
            ],
            "urls": url_results,
            "security_flags": security_flags,
            "cached_hit": False
        }

        # 2. Save result to local vector memory cache
        ThreatMemoryCache.set(text, result)
        return result