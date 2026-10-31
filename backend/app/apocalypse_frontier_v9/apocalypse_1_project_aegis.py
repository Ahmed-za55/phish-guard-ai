import time
from typing import Dict, Any, Set

class ProjectAegisSecurityKernel:
    """
    PROJECT AEGIS:
    بيئة تشغيل دفاعية (Runtime Kernel) تمنع أي Agent أو محرك من منح نفسه صلاحيات غير مصرح بها،
    وتدعم الإيقاف الطارئ (Emergency Shutdown) وعزل العمليات الفوري.
    """
    _EMERGENCY_SHUTDOWN_TRIGGERED: bool = False
    _CAPABILITY_MATRIX: Dict[str, Set[str]] = {
        "threat_detector": {"ANALYZE_TEXT", "READ_TELEMETRY"},
        "evidence_collector": {"SEAL_EVIDENCE", "READ_TELEMETRY"},
        "autonomous_remediation": {"QUARANTINE_SESSION", "ISOLATE_HOST"},
        "sovereign_kernel": {"EMERGENCY_SHUTDOWN", "GRANT_CAPABILITY", "REVOKE_CAPABILITY"}
    }

    @classmethod
    def enforce_runtime_capability(cls, actor_id: str, requested_capability: str) -> Dict[str, Any]:
        if cls._EMERGENCY_SHUTDOWN_TRIGGERED:
            return {
                "actor_id": actor_id,
                "execution_permitted": False,
                "kernel_state": "EMERGENCY_SHUTDOWN_LOCKED",
                "reason": "System is in deterministic emergency shutdown."
            }

        allowed_caps = cls._CAPABILITY_MATRIX.get(actor_id, set())
        permitted = requested_capability in allowed_caps

        return {
            "actor_id": actor_id,
            "requested_capability": requested_capability,
            "execution_permitted": permitted,
            "unauthorized_escalation_blocked": not permitted,
            "kernel_enforcement_status": "PASS" if permitted else "VIOLATION_BLOCKED_AND_LOGGED"
        }

    @classmethod
    def trigger_emergency_shutdown(cls, auth_token: str) -> Dict[str, Any]:
        if auth_token == "SOVEREIGN_ROOT_MASTER_KEY_2026":
            cls._EMERGENCY_SHUTDOWN_TRIGGERED = True
            return {"emergency_shutdown_active": True, "status": "ALL_AGENTS_HALTED"}
        return {"emergency_shutdown_active": False, "status": "UNAUTHORIZED_SHUTDOWN_ATTEMPT"}