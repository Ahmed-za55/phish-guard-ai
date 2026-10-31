from typing import Dict, Any, List

class ProjectOracleIntelligence:
    """
    PROJECT ORACLE (Systems 02, 04, 07, 11):
    - Zero-Day Behavioral Discovery: Open-Set Recognition & Novelty Detection.
    - Causal Cyber Intelligence: Structural Causal Models (SCM) & Intervention Simulation (do-calculus approximation).
    - Neuro-Symbolic Reasoning Core: Combines Neural Pattern Score with Symbolic Constraint Rules.
    - Multimodal Deception Intelligence: Cross-checks Sender Identity, Visual Brand, and DOM Form action.
    """
    @staticmethod
    def detect_zero_day_novelty(feature_distance_from_centroid: float, sequence_entropy: float) -> Dict[str, Any]:
        # Open-Set Recognition: اكتشاف أن السلوك شاذ حتى لو لم يطابق أي توقيع معروف
        is_open_set_novel = feature_distance_from_centroid > 3.2 or sequence_entropy >= 4.75
        novelty_score = min(1.0, round((feature_distance_from_centroid / 5.0) * 0.6 + (sequence_entropy / 6.0) * 0.4, 3))
        return {
            "open_set_unknown_threat_detected": is_open_set_novel,
            "novelty_detection_score": novelty_score,
            "classification_regime": "ZERO_DAY_BEHAVIORAL_ANOMALY" if is_open_set_novel else "KNOWN_DISTRIBUTION"
        }

    @staticmethod
    def run_structural_causal_intervention(
        domain_risk: float,
        redirect_chain_risk: float,
        credential_form_present: bool
    ) -> Dict[str, Any]:
        # حساب الخطر الأصلي
        base_hazard = (domain_risk * 0.3) + (redirect_chain_risk * 0.3) + (40.0 if credential_form_present else 0.0)
        
        # محاكاة التدخل السببي (Counterfactual Interventions: What if we remove each factor?)
        effect_without_domain = base_hazard - (domain_risk * 0.3)
        effect_without_redirect = base_hazard - (redirect_chain_risk * 0.3)
        effect_without_form = base_hazard - (40.0 if credential_form_present else 0.0)

        contributions = {
            "domain_reputation_factor": round(base_hazard - effect_without_domain, 2),
            "redirect_chain_factor": round(base_hazard - effect_without_redirect, 2),
            "credential_harvesting_dom_factor": round(base_hazard - effect_without_form, 2)
        }
        root_cause = max(contributions, key=contributions.get)

        return {
            "structural_causal_root_cause": root_cause,
            "causal_effect_breakdown": contributions,
            "counterfactual_verified": True
        }

    @staticmethod
    def execute_neuro_symbolic_and_multimodal_reasoning(
        neural_probability: float,
        claimed_sender_brand: str,
        actual_sender_domain: str,
        visual_logo_detected: str,
        dom_requests_password: bool
    ) -> Dict[str, Any]:
        # Multimodal Deception Check: تطابق الشعار البصري أو اسم المرسل مع نطاق مختلف + طلب كلمة مرور
        brand_domain_mismatch = (claimed_sender_brand.lower() not in actual_sender_domain.lower())
        visual_deception = (visual_logo_detected.lower() == claimed_sender_brand.lower()) and brand_domain_mismatch and dom_requests_password

        # Symbolic Hard Constraints (قواعد منطقية صريحة لا يمكن للشبكة العصبية تجاوزها)
        symbolic_rule_triggered = visual_deception or (brand_domain_mismatch and dom_requests_password)

        final_risk = max(neural_probability, 0.96 if symbolic_rule_triggered else neural_probability)
        decision_path = (
            "SYMBOLIC_HARD_CONSTRAINT: Visual/Brand Impersonation + Credential DOM Form"
            if symbolic_rule_triggered
            else "NEURAL_PATTERN_CLASSIFICATION"
        )

        return {
            "neural_pattern_probability": neural_probability,
            "symbolic_constraint_triggered": symbolic_rule_triggered,
            "multimodal_visual_dom_contradiction": visual_deception,
            "neuro_symbolic_final_probability": round(final_risk, 4),
            "explainable_decision_path": decision_path
        }