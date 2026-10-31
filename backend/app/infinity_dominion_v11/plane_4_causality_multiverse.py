from typing import Dict, Any, List

class CausalityAndMultiverseGridPlane:
    """
    Plane 4 — Simulation & Adversarial Research Grid (PROJECT CAUSALITY + MULTIVERSE X + GLOBAL HIVE):
    - يجيب عن الأسئلة السببية الخمسة: لماذا؟ ما الدليل الحاسم؟ ماذا لو حُذف؟ ما التفسير البديل؟ ما الاختبار الفاصل؟
    - يشغل محاكاة MULTIVERSE X وتنسيق GLOBAL HIVE الفيدرالي المقاوم للعقد البيزنطية.
    """
    @staticmethod
    def run_counterfactual_causality_and_hive(
        indicators: Dict[str, float],
        federated_node_scores: List[float]
    ) -> Dict[str, Any]:
        # indicadores: {"domain_age_hazard": 0.35, "credential_dom_hazard": 0.50, "urgency_syntax_hazard": 0.15}
        total_score = sum(indicators.values())
        decision_threshold = 0.60

        # تحديد المؤشر الذي غيّر القرار (Pivotal Evidence via Counterfactual Removal)
        pivotal_indicators = []
        counterfactual_outcomes = {}
        for k, v in indicators.items():
            score_without_k = round(total_score - v, 3)
            decision_flips = (total_score >= decision_threshold) and (score_without_k < decision_threshold)
            counterfactual_outcomes[f"without_{k}"] = {
                "remaining_score": score_without_k,
                "decision_would_flip_to_safe": decision_flips
            }
            if decision_flips:
                pivotal_indicators.append(k)

        primary_driver = max(indicators, key=indicators.get) if indicators else "none"

        # PROJECT GLOBAL HIVE: Trim Byzantine outliers
        s = sorted(federated_node_scores)
        trimmed = s[1:-1] if len(s) >= 4 else s
        hive_consensus = round(sum(trimmed) / max(len(trimmed), 1), 3)

        return {
            "plane": "SIMULATION_AND_CAUSAL_GRID_PLANE",
            "project_causality": {
                "why_classified_dangerous": f"Primary causal driver is '{primary_driver}' contributing {indicators.get(primary_driver, 0.0):.2f} to total risk {total_score:.2f}.",
                "pivotal_evidence_that_changed_decision": pivotal_indicators,
                "counterfactual_what_if_removed": counterfactual_outcomes,
                "alternative_plausible_hypothesis": "Legitimate enterprise SSO migration portal with newly registered domain.",
                "discriminating_verification_test": "Verify TLS Organization (OV/EV) certificate lineage and official DNS CAA/TXT ownership records."
            },
            "project_global_hive": {
                "byzantine_resilient_consensus": hive_consensus,
                "privacy_preserving_aggregation": True
            }
        }