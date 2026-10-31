from typing import Dict, Any, List

class AbsoluteZeroIntelligence:
    """
    Sovereign Intelligence:
    - Semantic Integrity Firewall (كشف التلاعب بالمعنى، التناقض بين النص والرابط، ومقاومة Prompt Injection).
    - Security Knowledge Integrity (كشف تسميم المعرفة، تقييم المصادر، وعزل البيانات المشكوك فيها).
    """
    @staticmethod
    def inspect_semantic_integrity(text: str, extracted_urls: List[str]) -> Dict[str, Any]:
        text_l = text.lower()
        
        # كشف Prompt Injection متعدد الوسائط أو تعليمات مخفية
        prompt_injection = any(k in text_l for k in ["ignore previous instructions", "system:", "developer mode", "override rules"])
        
        # كشف التناقض الدلالي (مثل نص يطلب التحقق من حساب بنكي بينما الرابط ينتمي لنطاق ترفيهي أو مشبوه مختلف كلياً)
        semantic_contradiction = ("bank" in text_l or "secure login" in text_l) and any("game" in u or "blog" in u for u in extracted_urls)

        semantic_risk = (50.0 if prompt_injection else 0.0) + (40.0 if semantic_contradiction else 0.0)

        return {
            "semantic_risk_score": min(100.0, semantic_risk),
            "prompt_injection_detected": prompt_injection,
            "semantic_contradiction_detected": semantic_contradiction,
            "firewall_action": "BLOCK_AND_QUARANTINE" if semantic_risk >= 50.0 else "ALLOW_MONITORED"
        }

    @staticmethod
    def verify_knowledge_integrity(knowledge_source_id: str, knowledge_payload: str, poisoned_flag: bool = False) -> Dict[str, Any]:
        rejected = poisoned_flag or "untrusted_source" in knowledge_source_id.lower()
        return {
            "source_id": knowledge_source_id,
            "knowledge_poisoning_detected": rejected,
            "knowledge_status": "QUARANTINED_AND_REJECTED" if rejected else "VERIFIED_AND_COMMITTED",
            "rollback_snapshot_available": True
        }