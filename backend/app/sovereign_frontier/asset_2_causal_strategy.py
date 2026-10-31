import math
from typing import Dict, Any, List

class CausalAndStrategyIntelligence:
    """
    الأصل الاستراتيجي الثاني:
    1. Intelligence Contamination Defense: يكتشف المصادر المسمومة أو المتناقضة ويعزلها قبل التحليل.
    2. Attack Strategy Reverse Engineering: يستنتج مراحل الحملة والخطوة القادمة مع حساب عدم اليقين (Shannon Entropy).
    3. Security Causal Intelligence: يحسب الأثر السببي الفعلي لكل عامل ويحدد التدخل الأصغر الكفيل بمنع الاختراق.
    """
    STAGE_TRANSITIONS = {
        "RECON_AND_LURE": {"CREDENTIAL_HARVEST": 0.72, "MALWARE_DROP": 0.20, "ABORT": 0.08},
        "CREDENTIAL_HARVEST": {"OAUTH_TOKEN_GRANT": 0.65, "SESSION_HIJACK": 0.28, "EXFILTRATION": 0.07},
        "OAUTH_TOKEN_GRANT": {"LATERAL_API_ABUSE": 0.58, "BEC_INVOICE_MANIPULATION": 0.35, "PERSISTENCE": 0.07},
        "SESSION_HIJACK": {"BEC_INVOICE_MANIPULATION": 0.62, "EXFILTRATION": 0.30, "PERSISTENCE": 0.08}
    }

    @classmethod
    def filter_contaminated_intelligence(cls, intel_reports: List[Dict[str, Any]]) -> Dict[str, Any]:
        """يكتشف المعلومات المسمومة عبر فحص انحراف ادعاء المصدر عن الإجماع الموزون بالسمعة."""
        if not intel_reports:
            return {"trusted_reports": [], "quarantined_sources": [], "contamination_detected": False}

        weighted_sum = sum(float(r["risk_claim"]) * float(r["source_reputation"]) for r in intel_reports)
        total_rep = sum(float(r["source_reputation"]) for r in intel_reports) or 1e-6
        consensus = weighted_sum / total_rep

        trusted = []
        quarantined = []
        for r in intel_reports:
            rep = float(r["source_reputation"])
            claim = float(r["risk_claim"])
            divergence = abs(claim - consensus)
            # مصدر ذو سمعة منخفضة أو ينحرف بشدة لتضليل النظام (Poisoning Attempt)
            if rep < 0.40 or (divergence > 0.55 and rep < 0.75):
                quarantined.append(r["source_id"])
            else:
                trusted.append(r)

        return {
            "consensus_risk_estimate": round(consensus, 4),
            "trusted_reports": trusted,
            "quarantined_sources": quarantined,
            "contamination_detected": len(quarantined) > 0
        }

    @classmethod
    def reverse_engineer_attack_strategy(cls, observed_stages: List[str], target_sector: str = "FINANCE") -> Dict[str, Any]:
        current_stage = observed_stages[-1] if observed_stages else "RECON_AND_LURE"
        next_dist = cls.STAGE_TRANSITIONS.get(current_stage, {"EXFILTRATION": 0.80, "PERSISTENCE": 0.20})

        # حساب إنتروبيا شانون لقياس عدم اليقين في الخطوة القادمة للمهاجم
        entropy = -sum(p * math.log2(p) for p in next_dist.values() if p > 0)
        max_entropy = math.log2(len(next_dist)) if len(next_dist) > 1 else 1.0
        normalized_uncertainty = round(entropy / max_entropy, 4)

        most_likely_next = max(next_dist, key=next_dist.get)
        return {
            "inferred_campaign_stages": observed_stages,
            "likely_adversary_objective": "FINANCIAL_WIRE_DIVERSION" if target_sector == "FINANCE" else "CREDENTIAL_AND_IP_THEFT",
            "predicted_next_stage": most_likely_next,
            "next_stage_probability_distribution": next_dist,
            "prediction_uncertainty_entropy": normalized_uncertainty
        }

    @staticmethod
    def compute_causal_interventions(causal_factors: Dict[str, float], breach_threshold: float = 0.60) -> Dict[str, Any]:
        """
        يطبق تحليل التدخل السببي (Counterfactual do-intervention):
        يحسب الخطر الإجمالي، ثم يختبر إزالة كل عامل على حدة لمعرفة أي تدخل سيمنع الاختراق فعلاً.
        """
        # دمج احتمالي غير خطي (Noisy-OR Causal Model): P(Breach) = 1 - prod(1 - c_i)
        prob_no_breach = 1.0
        for c in causal_factors.values():
            prob_no_breach *= (1.0 - min(0.99, max(0.0, c)))
        baseline_breach_prob = round(1.0 - prob_no_breach, 4)

        interventions = {}
        preventive_interventions = []

        for factor, val in causal_factors.items():
            rem_no_breach = 1.0
            for k, v in causal_factors.items():
                if k != factor:
                    rem_no_breach *= (1.0 - min(0.99, max(0.0, v)))
            new_prob = round(1.0 - rem_no_breach, 4)
            risk_drop = round(baseline_breach_prob - new_prob, 4)
            would_prevent = (baseline_breach_prob >= breach_threshold) and (new_prob < breach_threshold)

            interventions[f"do(remediate_{factor})"] = {
                "post_intervention_breach_prob": new_prob,
                "causal_risk_reduction": risk_drop,
                "prevents_breach_alone": would_prevent
            }
            if would_prevent:
                preventive_interventions.append(factor)

        root_driver = max(causal_factors, key=causal_factors.get) if causal_factors else "NONE"
        return {
            "baseline_breach_probability": baseline_breach_prob,
            "primary_causal_driver": root_driver,
            "counterfactual_interventions": interventions,
            "minimal_interventions_that_prevent_breach": preventive_interventions
        }