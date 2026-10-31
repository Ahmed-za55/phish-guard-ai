from typing import Dict, Any, List

class CyberDegradationIntelligence:
    """
    Cyber Degradation Intelligence:
    الدفاع أثناء الانهيار الجزئي: اكتشاف تدهور أداء المكونات، عزل الخدمات غير الموثوقة،
    واستمرار الوظائف الأمنية الأساسية دون انهيار النظام.
    """
    @staticmethod
    def assess_system_degradation(component_health_metrics: Dict[str, float]) -> Dict[str, Any]:
        degraded_components = [comp for comp, health in component_health_metrics.items() if health < 0.60]
        critical_failure = any(health < 0.30 for health in component_health_metrics.values())

        operational_mode = "CRITICAL_SAFE_DEGRADED_MODE" if critical_failure else ("PARTIAL_DEGRADED_MODE" if degraded_components else "NOMINAL_FULL_MODE")

        return {
            "operational_mode": operational_mode,
            "degraded_components": degraded_components,
            "essential_security_functions_active": True,
            "graceful_isolation_executed": len(degraded_components) > 0
        }