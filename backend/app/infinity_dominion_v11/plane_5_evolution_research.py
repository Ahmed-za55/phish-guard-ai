import math
from typing import Dict, Any, List

class EvolutionAutonomousResearchPlane:
    """
    Plane 5 — Independent Intelligence Research Plane (PROJECT EVOLUTION):
    - يختبر الفرضيات البحثية آلياً ويطبق اختبار الدلالة الإحصائية (Welch's t-test approximation).
    - يمنع ترقية أي نموذج Challenger إلا إذا تفوق إحصائياً على Champion دون رفع الإنذارات الكاذبة.
    """
    @staticmethod
    def evaluate_champion_vs_challenger(
        hypothesis_name: str,
        champion_f1_trials: List[float],
        challenger_f1_trials: List[float],
        challenger_fpr: float,
        max_allowed_fpr: float = 0.015
    ) -> Dict[str, Any]:
        n1, n2 = len(champion_f1_trials), len(challenger_f1_trials)
        m1 = sum(champion_f1_trials) / max(n1, 1)
        m2 = sum(challenger_f1_trials) / max(n2, 1)

        var1 = sum((x - m1) ** 2 for x in champion_f1_trials) / max(n1 - 1, 1)
        var2 = sum((x - m2) ** 2 for x in challenger_f1_trials) / max(n2 - 1, 1)

        se = math.sqrt((var1 / max(n1, 1)) + (var2 / max(n2, 1)) + 1e-12)
        t_stat = (m2 - m1) / se

        # t_stat > 2.10 يشير إلى دلالة إحصائية قوية (p < 0.05) لصالح النموذج الجديد
        statistically_significant_gain = (m2 > m1) and (t_stat > 2.10)
        fpr_within_bounds = challenger_fpr <= max_allowed_fpr
        promote = statistically_significant_gain and fpr_within_bounds

        return {
            "plane": "INDEPENDENT_INTELLIGENCE_RESEARCH_PLANE",
            "hypothesis_tested": hypothesis_name,
            "champion_mean_f1": round(m1, 4),
            "challenger_mean_f1": round(m2, 4),
            "welch_t_statistic": round(t_stat, 3),
            "statistically_significant": statistically_significant_gain,
            "fpr_budget_respected": fpr_within_bounds,
            "promotion_verdict": "PROMOTE_CHALLENGER_MODEL" if promote else "HOLD_CHAMPION_REJECT_CANDIDATE"
        }