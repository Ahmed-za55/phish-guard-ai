from typing import Dict, Any

class AdaptiveConstitutionAndEconomics:
    """
    4. Adaptive Security Constitution & Decision Economics:
    - يفرض شروط أمان حتمية ولا يسمح للذكاء الاصطناعي بتجاوز السياسات.
    - يحسب الخسارة المتوقعة (Expected Loss) للقرار الأمني (السماح، الحظر، الخطأ).
    """
    @staticmethod
    def evaluate_decision_economics(threat_probability: float, potential_impact_usd: float, false_positive_cost_usd: float) -> Dict[str, Any]:
        expected_loss_block = (1.0 - threat_probability) * false_positive_cost_usd
        expected_loss_allow = threat_probability * potential_impact_usd

        optimal_action = "BLOCK_THREAT" if expected_loss_allow >= expected_loss_block else "PERMIT_TRANSACTION"
        net_savings = abs(expected_loss_allow - expected_loss_block)

        return {
            "economics_framework": "EXPECTED_LOSS_CALCULUS",
            "threat_probability": threat_probability,
            "expected_loss_if_allowed_usd": round(expected_loss_allow, 2),
            "expected_loss_if_blocked_usd": round(expected_loss_block, 2),
            "optimal_economic_action": optimal_action,
            "justified_net_value_usd": round(net_savings, 2)
        }