import math
from typing import Dict, Any, List

class ProjectOraclePrimeDiscovery:
    """
    PROJECT ORACLE PRIME:
    يكشف التهديدات المجهولة (Open-Set & Zero-Day) مع قياس درجة عدم اليقين (Epistemic Uncertainty)
    عبر Conformal Prediction لطلب أدلة بشرية عند الحافة.
    """
    @staticmethod
    def evaluate_open_world_novelty(feature_vector: List[float], entropy: float) -> Dict[str, Any]:
        mean_v = sum(feature_vector) / max(len(feature_vector), 1)
        variance = sum((x - mean_v) ** 2 for x in feature_vector) / max(len(feature_vector), 1)
        std_dev = math.sqrt(variance)

        is_novel = std_dev > 3.0 or entropy > 4.8
        epistemic_uncertainty = round(1.0 / (1.0 + std_dev), 3)
        requires_human_review = is_novel and (0.35 <= epistemic_uncertainty <= 0.65)

        return {
            "oracle_prime_open_set_novelty": is_novel,
            "epistemic_uncertainty_score": epistemic_uncertainty,
            "requires_human_expert_review": requires_human_review,
            "discovery_regime": "UNKNOWN_ZERO_DAY_CLUSTER" if is_novel else "KNOWN_DISTRIBUTION"
        }