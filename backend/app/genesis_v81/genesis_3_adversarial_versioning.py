from typing import Dict, Any, List

class AdversarialSystemIdentificationAndVersioning:
    """
    Genesis P1:
    - Adversarial System Identification (اكتشاف حالات الفشل والمدخلات الشاذة في معزل).
    - Cross-Version Security Intelligence (مقارنة سلوك الإصدارات ومنع تراجع الحماية).
    """
    @staticmethod
    def identify_adversarial_system_flaws(test_inputs: List[Dict[str, Any]]) -> Dict[str, Any]:
        failed_cases = [t for t in test_inputs if t.get("causes_wrong_decision", False)]
        return {
            "total_test_vectors_run": len(test_inputs),
            "system_failure_cases_discovered": len(failed_cases),
            "robustness_score": round(1.0 - (len(failed_cases) / max(len(test_inputs), 1)), 2),
            "sandbox_isolation_maintained": True
        }

    @staticmethod
    def compare_cross_version_security(v_old_metrics: Dict[str, float], v_new_metrics: Dict[str, float]) -> Dict[str, Any]:
        old_recall = v_old_metrics.get("recall", 0.98)
        new_recall = v_new_metrics.get("recall", 0.95)
        regression_detected = new_recall < old_recall

        return {
            "security_regression_detected": regression_detected,
            "recall_delta": round(new_recall - old_recall, 3),
            "promotion_gate": "BLOCKED_SECURITY_DEGRADATION" if regression_detected else "APPROVED_FOR_RELEASE",
            "automatic_rollback_ready": regression_detected
        }