from typing import Dict, Any, Callable
import hashlib

class AdversarialAndResilienceLab:
    """
    مختبر التحايل والمرونة:
    1. يقارن أداء النموذج المعقد بقاعدة كشف بسيطة (Baseline Rule) لاكتشاف أي تراجع أو تحايل (Adversarial Drift).
    2. يوفر قاطع دائرة (Circuit Breaker) يعزل الأعطال ويشغل النظام محلياً بأمان إذا تعطل أي مكون.
    """
    @staticmethod
    def evaluate_adversarial_resilience(text: str, urls: list, complex_verdict_is_phishing: bool) -> Dict[str, Any]:
        # قاعدة كشف مرجعية بسيطة وموثوقة (Deterministic Baseline)
        simple_baseline_flag = any(
            u.get("risk_score", 0) >= 50 or "http://" in u.get("url", "")
            for u in urls
        ) or ("password" in text.lower() and "urgent" in text.lower())

        # إذا اكتشفت القاعدة البسيطة خطراً واضحاً بينما فشل النموذج المعقد، نسجل انحرافاً (Model Drift / Evasion)
        evasion_suspected = bool(simple_baseline_flag and not complex_verdict_is_phishing)

        return {
            "baseline_detector_triggered": simple_baseline_flag,
            "complex_model_triggered": complex_verdict_is_phishing,
            "adversarial_evasion_or_drift_detected": evasion_suspected,
            "promotion_gate_status": "HOLD_RETRAINING_REQUIRED" if evasion_suspected else "PASSED_QUALITY_GATE",
            "effective_safe_verdict": True if evasion_suspected else complex_verdict_is_phishing
        }

    @staticmethod
    def execute_with_circuit_breaker(component_name: str, func: Callable, *args, **kwargs) -> Dict[str, Any]:
        try:
            result = func(*args, **kwargs)
            return {"status": "healthy", "component": component_name, "data": result, "fallback_used": False}
        except Exception as exc:
            # عزل العطل وتشغيل الوضع المحلي الآمن دون إسقاط المنظومة
            return {
                "status": "isolated_fault_degraded_gracefully",
                "component": component_name,
                "error_type": type(exc).__name__,
                "fallback_used": True,
                "data": {"degraded_offline_mode": True}
            }