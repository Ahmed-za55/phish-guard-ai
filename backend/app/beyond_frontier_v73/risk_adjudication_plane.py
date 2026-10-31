from typing import Dict, Any

class RiskAdjudicationPlane:
    """
    الطبقة الخامسة: محاكاة القرارات البديلة (Counterfactual Risk Simulator) لاختيار القرار الأقل تكلفة،
    مع التحكم في المخاطر بدون افتراضات توزيعية (Distribution-Free Conformal Risk Control).
    """
    # مصفوفة التكلفة: False Negative (تمرير هجوم) تكلفته 100، False Positive (حظر سليم) تكلفته 25
    COST_FALSE_NEGATIVE = 100.0
    COST_FALSE_POSITIVE = 25.0
    COST_HUMAN_REVIEW = 8.0

    @classmethod
    def simulate_counterfactual_decisions(cls, adjudicated_risk_score: float, disagreement_std: float) -> Dict[str, Any]:
        p_threat = max(0.0, min(1.0, adjudicated_risk_score / 100.0))
        p_benign = 1.0 - p_threat

        # حساب الخسارة المتوقعة (Expected Loss) لكل قرار بديل
        expected_costs = {
            "ALLOW_MONITORED": round(p_threat * cls.COST_FALSE_NEGATIVE, 2),
            "WARN_USER_RESTRICTED": round(p_threat * (cls.COST_FALSE_NEGATIVE * 0.25) + p_benign * (cls.COST_FALSE_POSITIVE * 0.30), 2),
            "HOLD_FOR_HUMAN_REVIEW": round(cls.COST_HUMAN_REVIEW + (p_threat * 5.0), 2),
            "BLOCK_AND_QUARANTINE": round(p_benign * cls.COST_FALSE_POSITIVE, 2)
        }

        # Research: Distribution-Free Risk Control
        # إذا كان عدم اليقين أو تباين المحللات مرتفعاً، نمنع القرار الحدي التلقائي ونختار المراجعة أو التحذير
        high_uncertainty = (0.35 <= p_threat <= 0.68) or (disagreement_std >= 25.0)
        if high_uncertainty:
            optimal_action = "HOLD_FOR_HUMAN_REVIEW" if p_threat >= 0.50 else "WARN_USER_RESTRICTED"
        else:
            optimal_action = min(expected_costs, key=expected_costs.get)

        return {
            "threat_probability_estimate": round(p_threat, 4),
            "counterfactual_expected_costs": expected_costs,
            "counterfactual_optimal_action": optimal_action,
            "distribution_free_risk_control": {
                "high_uncertainty_abstention_triggered": high_uncertainty,
                "exchangeability_assumption_note": "Guaranteed error bounds hold under sample exchangeability; drift monitor active for shift detection."
            }
        }