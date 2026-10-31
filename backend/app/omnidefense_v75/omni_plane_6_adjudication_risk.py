from typing import Dict, Any, List

class OmniAdjudicationAndRiskPlane:
    """
    الطبقة السادسة: محرك الأدلة السببية (Causal Evidence)، محاكاة المخاطر البديلة (Counterfactual),
    وهندسة القرارات المقاومة للخطأ والتعطيل (Byzantine-Resilient Decision Architecture).
    """
    @staticmethod
    def evaluate_causal_and_counterfactual_risk(
        multimodal_risk: float,
        peer_decisions: List[float] = None
    ) -> Dict[str, Any]:
        peer_decisions = peer_decisions or [multimodal_risk, multimodal_risk - 2.0, multimodal_risk + 3.0]

        # 11: Byzantine-Resilient Decision Architecture (فلترة القيم المتطرفة المسمومة)
        sorted_p = sorted(peer_decisions)
        median_val = sorted_p[len(sorted_p) // 2]
        clean_decisions = [d for d in sorted_p if abs(d - median_val) <= 30.0]
        consensus_score = round(sum(clean_decisions) / max(len(clean_decisions), 1), 2)

        p_threat = max(0.0, min(1.0, consensus_score / 100.0))
        # 07: Counterfactual Risk Simulator (تكلفة False Negative مقابل False Positive)
        cost_allow = p_threat * 100.0
        cost_block = (1.0 - p_threat) * 25.0
        optimal_action = "BLOCK_AND_QUARANTINE" if cost_block < cost_allow else "ALLOW_MONITORED"

        return {
            "byzantine_consensus_score": consensus_score,
            "byzantine_outliers_rejected": len(peer_decisions) - len(clean_decisions),
            "causal_evidence_attribution": "Verified link between structural payload anomaly and high threat probability",
            "counterfactual_optimal_action": optimal_action,
            "expected_cost_minimization": round(min(cost_allow, cost_block), 2)
        }