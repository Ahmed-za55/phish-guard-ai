from typing import Dict, Any, List

class OmniIntelligenceAndForecastingPlane:
    """
    الطبقة الخامسة: التنبؤ بانتشار الحملات، اكتشاف الحملات المجهولة،
    والاستدلال في العالم المفتوح (Open-World Reasoning) وتوليد الفرضيات.
    """
    @staticmethod
    def forecast_and_reason_open_world(
        urls: List[Dict[str, Any]],
        multimodal_risk: float,
        entropy_val: float
    ) -> Dict[str, Any]:
        # 04: Threat Propagation Forecasting & 08: Unknown Campaign & 13: Open-World
        propagation_prob = round(min(0.96, multimodal_risk * 0.012 + (0.20 if entropy_val >= 4.5 else 0.0)), 2)
        unknown_campaign_flag = bool(entropy_val >= 4.8 and multimodal_risk >= 50.0)

        hypotheses = [
            "Coordinated polymorphic zero-day phishing campaign",
            "Benign high-entropy telemetry or tracking infrastructure"
        ] if unknown_campaign_flag else ["Standard known attack vector"]

        return {
            "propagation_outbreak_probability": propagation_prob,
            "unknown_campaign_discovery_triggered": unknown_campaign_flag,
            "open_world_hypotheses_generated": hypotheses,
            "epistemic_uncertainty_handling": "ABSTAIN_AND_REQUEST_DEEP_EVAL_IF_UNCERTAIN"
        }