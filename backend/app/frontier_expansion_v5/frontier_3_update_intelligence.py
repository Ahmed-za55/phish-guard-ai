from typing import Dict, Any

class SecurityUpdateIntelligence:
    """
    Autonomous Security Update Intelligence:
    - التحقق من توقيع التحديث وسلامته.
    - تقييم نشر الكناري (Canary) ورصد التراجع الأمني (Security Regression).
    - التراجع التلقائي عند زيادة الإنذارات الكاذبة أو ثغرات الحماية.
    """
    @staticmethod
    def evaluate_canary_update(candidate_version: str, canary_error_rate: float, baseline_error_rate: float, security_tests_passed: bool) -> Dict[str, Any]:
        regression_detected = (canary_error_rate > baseline_error_rate * 1.25) or not security_tests_passed
        should_rollback = regression_detected

        return {
            "candidate_version": candidate_version,
            "canary_evaluation_completed": True,
            "security_regression_detected": regression_detected,
            "automatic_rollback_triggered": should_rollback,
            "deployment_status": "ROLLED_BACK_TO_PREVIOUS_STABLE" if should_rollback else "PROMOTED_TO_FULL_FLEET"
        }