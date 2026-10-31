from typing import Dict, Any, List

class ExperienceAndReliabilityIntelligence:
    """
    1. Human-Centric Intelligence & Economics: تفسير بلغة واضحة + تخصيص عمق التحليل.
    2. Cyber Service Reliability: التدهور المحكوم والتحقق من ادعاءات الحماية.
    """
    @staticmethod
    def generate_explainable_warning(raw_text: str, risk_score: float) -> Dict[str, Any]:
        reasons = []
        if "urgent" in raw_text.lower() or "immediately" in raw_text.lower():
            reasons.append("Coercive urgency detected (pressure to act fast)")
        if "password" in raw_text.lower() or "verify" in raw_text.lower():
            reasons.append("Credential harvesting lure detected")

        explanation_en = " ".join(reasons) if reasons else "Anomalous patterns inconsistent with standard communication."
        
        # تحكم تكيفي في عمق التحليل بناءً على مستوى الخطورة
        analysis_depth = "DEEP_FORENSIC" if risk_score >= 70.0 else ("BALANCED" if risk_score >= 30.0 else "LIGHTWEIGHT_FAST")

        return {
            "risk_score": risk_score,
            "human_readable_explanation": explanation_en,
            "cognitive_load_level": "OPTIMIZED_MINIMAL",
            "adaptive_analysis_depth": analysis_depth
        }

    @staticmethod
    def verify_service_resilience(failing_dependencies: List[str]) -> Dict[str, Any]:
        # استمرار الحماية الأساسية حتى لو تعطلت خدمات التحليل الثانوية
        non_critical = {"reputation_cache", "analytics_exporter"}
        is_critical_outage = any(d not in non_critical for d in failing_dependencies)

        return {
            "active_outages": failing_dependencies,
            "graceful_degradation_active": len(failing_dependencies) > 0,
            "core_protection_intact": not is_critical_outage,
            "operational_mode": "FAIL_SAFE_CORE_DEFENSE" if len(failing_dependencies) > 0 else "NOMINAL_FULL"
        }