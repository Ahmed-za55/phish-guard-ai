import hashlib
from typing import Dict, Any, List

class CyberImmuneAndDeceptionEngine:
    """
    P2 & P4 + Tech 1 (Neuro-Symbolic AI) + Tech 3 (Online Learning with Safety Constraints):
    - 01. Cyber Immune System: خط أساس طبيعي، ذاكرة مناعية للحوادث، استجابة متدرجة، ورفض التغذية غير الموثوقة.
    - 06. Deception-Aware Detection: كشف محاولات تضليل المصنف، فحص التناقض بين الإشارات، وسجل التضليل.
    """
    _IMMUNE_INCIDENT_MEMORY: Dict[str, int] = {}
    _DECEPTION_ATTEMPT_LOG: List[Dict[str, Any]] = []
    _BASELINE_ENTROPY_MEAN = 3.6

    @classmethod
    def evaluate_cyber_immune_response(
        cls,
        payload_signature: str,
        observed_entropy: float,
        neural_score: float,
        symbolic_axioms_triggered: List[str],
        feedback_source_trusted: bool = False
    ) -> Dict[str, Any]:
        # Tech 1: Neuro-Symbolic AI — الجمع بين الشبكة العصبية والقواعد المنطقية الصارمة
        symbolic_boost = 25.0 * len(symbolic_axioms_triggered)
        neuro_symbolic_confidence = round(min(1.0, (neural_score * 0.65 + symbolic_boost) / 100.0), 4)

        # حساب الانحراف عن خط الأساس الطبيعي (Self vs Non-Self Deviation)
        baseline_deviation = round(max(0.0, observed_entropy - cls._BASELINE_ENTROPY_MEAN), 3)
        repeat_encounters = cls._IMMUNE_INCIDENT_MEMORY.get(payload_signature, 0)

        if neuro_symbolic_confidence >= 0.70 or baseline_deviation >= 1.1:
            cls._IMMUNE_INCIDENT_MEMORY[payload_signature] = repeat_encounters + 1

        # استجابة مناعية متدرجة حسب مستوى الثقة والذاكرة السابقة
        if neuro_symbolic_confidence >= 0.85 or repeat_encounters >= 2:
            graduated_tier = "TIER_3_ADAPTIVE_QUARANTINE_AND_MEMORY_LOCK"
        elif neuro_symbolic_confidence >= 0.50 or baseline_deviation >= 0.8:
            graduated_tier = "TIER_2_ELEVATED_INSPECTION_AND_STEP_UP_AUTH"
        else:
            graduated_tier = "TIER_1_HOMEOSASIS_PASSIVE_MONITORING"

        # Tech 3: Online Learning with Safety Constraints
        online_update_applied = bool(feedback_source_trusted and neuro_symbolic_confidence >= 0.80)

        return {
            "baseline_entropy_deviation": baseline_deviation,
            "immune_memory_prior_encounters": repeat_encounters,
            "neuro_symbolic_fusion": {
                "neural_component_score": neural_score,
                "symbolic_logical_rules_matched": symbolic_axioms_triggered,
                "combined_neuro_symbolic_confidence": neuro_symbolic_confidence
            },
            "graduated_immune_response_tier": graduated_tier,
            "constrained_online_learning": {
                "untrusted_feedback_rejected": not feedback_source_trusted,
                "safe_incremental_update_committed": online_update_applied
            }
        }

    @classmethod
    def detect_adversarial_deception(cls, text: str, url_risk: float, browser_risk: float) -> Dict[str, Any]:
        # 06: Deception-Aware Detection — كشف المدخلات المصممة لإرباك التصنيف (مثل حشو كلمات آمنة أو محارف خفية)
        zero_width_count = sum(1 for c in text if ord(c) in {0x200B, 0x200C, 0x200D, 0xFEFF})
        benign_word_stuffing = text.lower().count("safe") + text.lower().count("official") >= 3
        signal_contradiction = abs(url_risk - browser_risk) >= 55.0

        deception_detected = bool(zero_width_count > 0 or (benign_word_stuffing and url_risk >= 45.0) or signal_contradiction)
        if deception_detected:
            entry_id = hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]
            cls._DECEPTION_ATTEMPT_LOG.append({
                "deception_id": entry_id,
                "zero_width": zero_width_count,
                "contradiction": signal_contradiction
            })

        return {
            "classifier_deception_detected": deception_detected,
            "inter_signal_contradiction_flagged": signal_contradiction,
            "evasion_stuffing_or_invisible_chars": bool(zero_width_count > 0 or benign_word_stuffing),
            "evidence_reliability_weight": 0.60 if deception_detected else 0.98,
            "logged_deception_attempts_total": len(cls._DECEPTION_ATTEMPT_LOG)
        }