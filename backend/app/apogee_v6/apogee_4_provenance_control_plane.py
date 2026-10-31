import time
import hashlib
import json
from typing import Dict, Any, List, Set

class DecisionProvenanceAndControlPlane:
    """
    1. Security Decision Provenance: توثيق كامل لسلسلة الأدلة، التوقيت، إصدار المحرك، وإصدار السياسة.
    2. Sovereign Intelligence Control Plane: التحكم في صلاحيات المحركات، منع التوسيع الذاتي للصلاحيات، وعزل المحركات الشاذة.
    """
    _ISOLATED_ENGINES: Set[str] = set()
    _ALLOWED_ENGINE_ACTIONS: Set[str] = {"ANALYZE", "SCORE", "RECOMMEND_CONTAINMENT", "REQUEST_REVIEW"}

    @classmethod
    def enforce_intelligence_control_plane(cls, engine_id: str, requested_action: str, cpu_quota_pct: float) -> Dict[str, Any]:
        if engine_id in cls._ISOLATED_ENGINES:
            return {"permitted": False, "status": "ENGINE_ISOLATED", "enforced_action": "NONE"}

        privilege_escalation_attempt = requested_action not in cls._ALLOWED_ENGINE_ACTIONS
        quota_exceeded = cpu_quota_pct > 80.0

        if privilege_escalation_attempt or quota_exceeded:
            cls._ISOLATED_ENGINES.add(engine_id)
            return {
                "engine_id": engine_id,
                "permitted": False,
                "self_privilege_escalation_blocked": privilege_escalation_attempt,
                "engine_isolated_automatically": True,
                "human_approval_required_for_reset": True
            }

        return {
            "engine_id": engine_id,
            "permitted": True,
            "self_privilege_escalation_blocked": False,
            "engine_isolated_automatically": False,
            "enforced_action": requested_action
        }

    @staticmethod
    def build_decision_provenance_record(
        decision_verdict: str,
        confidence: float,
        evidence_list: List[Dict[str, Any]],
        engine_version: str = "Apogee-Engine-v6.0",
        policy_version: str = "Sovereign-Policy-2026.10"
    ) -> Dict[str, Any]:
        record_body = {
            "decision_verdict": decision_verdict,
            "confidence_score": confidence,
            "evidence_chain": evidence_list,
            "engine_version": engine_version,
            "policy_version": policy_version,
            "timestamp_utc": int(time.time()),
            "retention_policy": "365_DAYS_IMMUTABLE_AUDIT"
        }
        provenance_hash = hashlib.sha256(json.dumps(record_body, sort_keys=True).encode()).hexdigest()
        return {
            **record_body,
            "tamper_evident_provenance_hash": provenance_hash
        }