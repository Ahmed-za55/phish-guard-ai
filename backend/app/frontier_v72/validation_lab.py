from typing import Dict, Any, List

class ContinuousValidationAndTwinLab:
    """
    الطبقة الرابعة: التوأم الرقمي التنبؤي (حساب المخاطر المتبقية)، الدفاع العدائي التكيفي،
    ومختبر التحقق الأمني المستمر لمنع تراجع الأمان قبل النشر.
    """
    CRITICAL_DOMAINS = {"localhost", "127.0.0.1", "kfs.edu.eg", "github.com", "sovereign.internal"}

    @classmethod
    def run_predictive_digital_twin(cls, initial_risk: float, proposed_action: str, urls: List[Dict[str, Any]]) -> Dict[str, Any]:
        # حساب انخفاض المخاطر بناءً على السياسة المقترحة داخل التوأم الرقمي
        mitigation_factors = {
            "BLOCK_AND_QUARANTINE": 0.95,
            "WARN_USER_RESTRICTED": 0.65,
            "HOLD_FOR_HUMAN_REVIEW_OR_DEEP_SCAN": 0.80,
            "ALLOW_MONITORED": 0.10
        }
        factor = mitigation_factors.get(proposed_action, 0.50)
        residual_risk = round(initial_risk * (1.0 - factor), 2)

        # فحص السلامة: رفض التغيير إذا كان يعطل نطاقاً حيوياً أو يترك مخاطر متبقية مرتفعة جداً
        hits_critical = any(any(c in u.get("url", "").lower() for c in cls.CRITICAL_DOMAINS) for u in urls)
        safety_test_passed = (not hits_critical) and (residual_risk <= 35.0 or initial_risk < 40.0)

        approved_action = proposed_action if safety_test_passed else "WARN_USER_RESTRICTED"
        return {
            "initial_risk_score": initial_risk,
            "simulated_action": proposed_action,
            "residual_risk_after_response": residual_risk,
            "safety_test_passed": safety_test_passed,
            "twin_approved_action": approved_action
        }

    @staticmethod
    def evaluate_adaptive_adversarial_and_ci_gate(text: str, urls: List[Dict[str, Any]], model_verdict: bool) -> Dict[str, Any]:
        # قياس تغير توزيع البيانات (Distribution Shift / OOD) عبر نسبة المحارف غير القياسية
        non_ascii_ratio = sum(1 for ch in text if ord(ch) > 127) / max(len(text), 1)
        distribution_shift_detected = non_ascii_ratio > 0.25

        # اختبار خط الأساس (Regression Baseline) لمنع تراجع النسخة
        baseline_phish = any(u.get("risk_score", 0) >= 55 for u in urls)
        regression_detected = (baseline_phish and not model_verdict)

        release_gate_passed = not regression_detected
        return {
            "distribution_shift_score": round(non_ascii_ratio, 4),
            "covariate_shift_alert": distribution_shift_detected,
            "adversarial_evasion_regression": regression_detected,
            "alternate_shadow_model_ready": True,
            "continuous_validation_release_gate": "APPROVED_FOR_PRODUCTION" if release_gate_passed else "BLOCKED_REGRESSION_DETECTED"
        }