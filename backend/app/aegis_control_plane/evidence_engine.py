from typing import Dict, Any, List
import hashlib

class EvidenceDecisionEngine:
    """
    يفصل بين الأدلة الجنائية القاطعة (Hard Evidence) والتوقعات الاحتمالية (Predictions)،
    يوثق إصدار السياسة والنموذج، ويوفر آلية لمراجعة القرار وتقليل الإنذارات الكاذبة.
    """
    MODEL_VERSION = "PhishGuard-Core-v71.0"
    POLICY_SCHEMA_VERSION = "AEGIS-Policy-2026.10"

    @classmethod
    def evaluate_decision(cls, signal_graph: Dict[str, Any], raw_evidence: List[str], model_prediction_confidence: float) -> Dict[str, Any]:
        hard_facts = [e for e in raw_evidence if any(k in e for k in ["Punycode", "AST", "Levenshtein", "Entropy"])]
        heuristic_inferences = [e for e in raw_evidence if e not in hard_facts]

        correlated_risk = signal_graph["correlated_risk_score"]
        
        # منع الإنذارات الكاذبة: التغاضي عن الإشارات اللغوية المنفردة إذا لم يدعمها رابط مشبوه أو دليل صلب
        false_positive_suppressed = False
        if correlated_risk < 35.0 and len(hard_facts) == 0:
            verdict = "ALLOW_MONITORED"
            is_phishing_verified = False
            if heuristic_inferences:
                false_positive_suppressed = True
        elif correlated_risk >= 75.0 or len(hard_facts) >= 2:
            verdict = "BLOCK_AND_QUARANTINE"
            is_phishing_verified = True
        else:
            verdict = "WARN_USER_RESTRICTED"
            is_phishing_verified = True

        decision_rationale = (
            f"Verdict '{verdict}' derived from {len(hard_facts)} hard forensic facts and "
            f"{len(heuristic_inferences)} heuristic signals (Correlated Score: {correlated_risk}/100)."
        )

        appeal_token = hashlib.sha256(f"{verdict}:{correlated_risk}:{cls.POLICY_SCHEMA_VERSION}".encode()).hexdigest()[:16]

        return {
            "verified_is_phishing": is_phishing_verified,
            "recommended_verdict": verdict,
            "decision_rationale": decision_rationale,
            "forensic_separation": {
                "hard_cryptographic_and_structural_facts": hard_facts,
                "probabilistic_heuristic_inferences": heuristic_inferences,
                "raw_model_prediction_confidence": model_prediction_confidence
            },
            "false_positive_guard_triggered": false_positive_suppressed,
            "version_metadata": {
                "model_version": cls.MODEL_VERSION,
                "policy_version": cls.POLICY_SCHEMA_VERSION
            },
            "appeal_and_review": {
                "reviewable": True,
                "appeal_reference_id": f"rev_{appeal_token}",
                "override_instructions": "Submit appeal_reference_id to Security Operations to whitelist or re-evaluate."
            }
        }