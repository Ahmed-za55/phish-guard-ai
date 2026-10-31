from typing import Dict, Any, List

class ThreatIntelligencePlane:
    """
    الطبقة الرابعة: إعادة بناء مسار الهجوم مع تحديد الأدلة المفقودة والفرضيات البديلة،
    استنتاج التسلسل السببي، والتنبؤ المبكر بانتشار الحملات.
    """
    @staticmethod
    def reconstruct_attack_path_and_causality(
        urls: List[Dict[str, Any]],
        urgency_present: bool,
        ast_present: bool,
        homograph_present: bool
    ) -> Dict[str, Any]:
        # 04: Attack-Path Reconstruction
        observed_nodes = []
        missing_evidence_gaps = []

        if urgency_present:
            observed_nodes.append("Initial_Lure_Social_Engineering")
        else:
            missing_evidence_gaps.append("No social engineering lure text observed (possible direct link share)")

        if urls:
            observed_nodes.append("Delivery_URL_Vector")
            missing_evidence_gaps.append("TLS certificate age and live HTTP redirect chain not fetched in offline mode")
        else:
            missing_evidence_gaps.append("No explicit URL extracted from payload")

        if homograph_present:
            observed_nodes.append("Visual_Brand_Impersonation")

        if ast_present:
            observed_nodes.append("Client_Side_Script_Exploitation")

        # البدائل التفسيرية (Competing Hypotheses) لمنع الثقة الزائفة
        alternative_explanations = [
            "Legitimate urgent administrative notification with non-standard formatting",
            "Automated marketing link with high-entropy tracking parameters"
        ] if len(observed_nodes) <= 2 else ["Multi-stage coordinated phishing campaign"]

        # Research: Causal Threat Discovery & Early-Warning Forecasting
        causal_confidence = round(min(0.95, len(observed_nodes) * 0.28), 2)
        early_warning_score = round(
            0.85 if (homograph_present or (urls and urgency_present)) else 0.15, 2
        )

        return {
            "reconstructed_attack_sequence": observed_nodes,
            "missing_evidence_gaps": missing_evidence_gaps,
            "competing_alternative_hypotheses": alternative_explanations,
            "causal_discovery_score": causal_confidence,
            "early_warning_campaign_forecast": {
                "pre_reputation_outbreak_probability": early_warning_score,
                "early_warning_triggered": early_warning_score >= 0.70
            }
        }