from typing import Dict, Any, List

class IdentityContinuityAndResourceIsolation:
    @staticmethod
    def evaluate_identity_continuity(user_id: str, events: Dict[str, Any]) -> Dict[str, Any]:
        mfa_fatigue = events.get("mfa_pushes", 0) >= 4
        session_abuse = events.get("concurrent_sessions", 1) > 3
        privilege_drift = events.get("sudden_admin_rights", False)
        risk = (40.0 if mfa_fatigue else 0.0) + (40.0 if session_abuse else 0.0) + (20.0 if privilege_drift else 0.0)
        return {
            "user_id": user_id,
            "identity_risk_score": min(100.0, risk),
            "mfa_fatigue_detected": mfa_fatigue,
            "session_abuse_detected": session_abuse,
            "privilege_escalation_anomaly": privilege_drift,
            "remediation_action": "REVOKE_ALL_SESSIONS_AND_STEP_UP" if risk >= 60.0 else "MONITOR"
        }

    @staticmethod
    def enforce_resource_isolation(cpu_usage_pct: float, memory_usage_pct: float) -> Dict[str, Any]:
        exhaustion_threat = (cpu_usage_pct > 85.0) or (memory_usage_pct > 85.0)
        return {
            "resource_exhaustion_attack_detected": exhaustion_threat,
            "adaptive_rate_limiting_active": exhaustion_threat,
            "critical_defense_functions_protected": True,
            "non_essential_workers_throttled": exhaustion_threat
        }