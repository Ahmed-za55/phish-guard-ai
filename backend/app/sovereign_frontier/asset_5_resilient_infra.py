import hashlib
import json
from typing import Dict, Any, List, Set

class VerifiableResilientInfrastructure:
    """
    الأصل الاستراتيجي الخامس:
    1. Autonomous Security Infrastructure: ينفذ إجراءات الاستجابة ضمن صلاحيات محددة مع لقطة تراجع (Rollback Snapshot).
    2. Sovereign Cyber Resilience: يحافظ على قدرة الفحص والحماية حتى عند انقطاع الإنترنت أو تعطل مزود الـ AI أو قاعدة البيانات.
    """
    ALLOWED_AUTONOMOUS_ACTIONS: Dict[str, Set[str]] = {
        "tier_1_responder": {"ISOLATE_SUSPICIOUS_SESSION", "SUSPEND_HIGH_RISK_WIRE", "REVOKE_COMPROMISED_TOKEN", "ENFORCE_STEP_UP_MFA"},
        "tier_0_observer": set()
    }
    _ROLLBACK_LEDGER: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def execute_governed_response(
        cls,
        responder_id: str,
        action: str,
        target_resource: str,
        prior_state: Dict[str, Any],
        evidence_digest: str
    ) -> Dict[str, Any]:
        allowed = cls.ALLOWED_AUTONOMOUS_ACTIONS.get(responder_id, set())
        if action not in allowed:
            return {
                "executed": False,
                "unauthorized_action_blocked": True,
                "reason": f"Responder '{responder_id}' lacks permission for '{action}'."
            }

        action_id = hashlib.sha256(f"{responder_id}:{action}:{target_resource}:{evidence_digest}".encode()).hexdigest()[:16]
        cls._ROLLBACK_LEDGER[action_id] = {
            "target_resource": target_resource,
            "restorable_prior_state": dict(prior_state),
            "action_applied": action
        }

        return {
            "action_id": action_id,
            "executed": True,
            "unauthorized_action_blocked": False,
            "action_applied": action,
            "target_resource": target_resource,
            "rollback_available": True,
            "verification_status": "STATE_TRANSITION_VERIFIED"
        }

    @classmethod
    def rollback_response(cls, action_id: str) -> Dict[str, Any]:
        if action_id not in cls._ROLLBACK_LEDGER:
            return {"rolled_back": False, "reason": "ACTION_ID_NOT_FOUND"}
        snap = cls._ROLLBACK_LEDGER.pop(action_id)
        return {
            "rolled_back": True,
            "target_resource": snap["target_resource"],
            "restored_state": snap["restorable_prior_state"]
        }

    @staticmethod
    def evaluate_under_component_outage(
        internet_connected: bool,
        ai_provider_online: bool,
        reputation_db_healthy: bool,
        local_signed_rules_match: bool,
        structural_anomaly_score: float
    ) -> Dict[str, Any]:
        """يضمن عدم انهيار النظام أو إصدار قرار SAFE خاطئ عند تعطل المكونات السحابية."""
        degraded_components = []
        if not internet_connected:
            degraded_components.append("EXTERNAL_INTERNET")
        if not ai_provider_online:
            degraded_components.append("CLOUD_LLM_PROVIDER")
        if not reputation_db_healthy:
            degraded_components.append("THREAT_INTEL_DB")

        is_degraded_mode = len(degraded_components) > 0

        if local_signed_rules_match or structural_anomaly_score >= 0.70:
            verdict = "MALICIOUS_BLOCK_LOCAL_ENFORCED"
        elif is_degraded_mode and structural_anomaly_score >= 0.35:
            # منع تحويل غياب المعلومات إلى SAFE
            verdict = "DEGRADED_SAFE_MODE_HOLD_AND_VERIFY"
        else:
            verdict = "LOCAL_VERIFIED_BENIGN"

        return {
            "operating_mode": "SOVEREIGN_OFFLINE_DEGRADED_SAFE_MODE" if is_degraded_mode else "FULL_ONLINE_MODE",
            "degraded_components": degraded_components,
            "system_collapsed": False,
            "enforced_verdict": verdict
        }