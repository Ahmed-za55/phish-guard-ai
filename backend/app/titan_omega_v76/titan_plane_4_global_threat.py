from typing import Dict, Any, List
import hashlib

class TitanGlobalThreatIntelligencePlane:
    """
    الطبقة الرابعة: البصمة الجينية الرقمية للحملات (Global Threat Genome) وإشارات ما قبل الهجوم (Pre-Attack).
    """
    @staticmethod
    def analyze_threat_genome_and_pre_attack(urls: List[Dict[str, Any]], urgency_present: bool) -> Dict[str, Any]:
        domain_stems = [u.get("url", "").split("//")[-1].split("/")[0][:6] for u in urls]
        genome_signature = hashlib.sha256("".join(sorted(domain_stems)).encode("utf-8")).hexdigest()[:16]

        pre_attack_signal = bool(urgency_present and len(urls) >= 1)

        return {
            "global_threat_genome_signature": f"gen_{genome_signature}",
            "campaign_family_cluster": "FAMILY_POLYMORPHIC_PHISH_01",
            "pre_attack_early_signal_detected": pre_attack_signal,
            "infrastructure_reusability_index": 0.85 if len(urls) > 0 else 0.10
        }