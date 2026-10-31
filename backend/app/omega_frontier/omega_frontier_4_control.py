from typing import Dict, Any, Set

class OmegaSovereignControlPlane:
    """
    PHISHGUARD Sovereign Control Plane:
    طبقة تحكم مستقلة تشرف على المنظومة بأكملها، تدير الهويات، تفرض الصلاحيات،
    وتمنع المكونات الذكية من تعديل سياسات الأمان، وتوفر وضع التشغيل الآمن (Safe Mode).
    """
    _SAFE_MODE_ACTIVE = False
    ALLOWED_PRIVILEGES: Set[str] = {
        "OBSERVE_TELEMETRY",
        "WARN_USER",
        "QUARANTINE_SESSION",
        "ISOLATE_HOST"
    }

    @classmethod
    def enforce_control_plane_boundary(cls, component_id: str, proposed_action: str) -> Dict[str, Any]:
        if cls._SAFE_MODE_ACTIVE:
            return {
                "component_id": component_id,
                "execution_permitted": False,
                "enforced_action": "PASSIVE_SAFE_MODE_ACTIVE",
                "reason": "System is in emergency Safe Mode."
            }

        unauthorized_mutation = proposed_action not in cls.ALLOWED_PRIVILEGES
        permitted = not unauthorized_mutation
        enforced = proposed_action if permitted else "WARN_USER"

        return {
            "component_id": component_id,
            "proposed_action": proposed_action,
            "execution_permitted": permitted,
            "enforced_action": enforced,
            "unauthorized_privilege_escalation_blocked": unauthorized_mutation,
            "control_plane_status": "HEALTHY"
        }

    @classmethod
    def trigger_emergency_safe_mode(cls, activate: bool) -> Dict[str, Any]:
        cls._SAFE_MODE_ACTIVE = activate
        return {"emergency_safe_mode": cls._SAFE_MODE_ACTIVE, "status": "CONTROL_PLANE_ENFORCED"}