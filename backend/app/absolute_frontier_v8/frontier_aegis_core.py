from typing import Dict, Any, Set

class ProjectAegisCoreRuntime:
    """
    PROJECT AEGIS CORE:
    بيئة تشغيل دفاعية تدير دورة حياة الوكلاء وتفرض سياسات صلاحيات دقيقة (Capability-Based Security)
    وتعزل العمليات المشبوهة فورياً.
    """
    _ACTIVE_CAPABILITIES: Dict[str, Set[str]] = {
        "genesis_agent": {"DISCOVER_ANOMALY", "EMIT_HYPOTHESIS"},
        "omniscience_agent": {"REASON_CROSS_MODAL", "PARSE_DOM"},
        "orchestrator_core": {"EVALUATE_ALL", "ENFORCE_POLICY"}
    }
    _QUARANTINED_AGENTS: Set[str] = set()

    @classmethod
    def enforce_runtime_capability(cls, agent_id: str, capability: str) -> Dict[str, Any]:
        if agent_id in cls._QUARANTINED_AGENTS:
            return {"permitted": False, "reason": "AGENT_QUARANTINED", "enforced_action": "BLOCK"}

        allowed = cls._ACTIVE_CAPABILITIES.get(agent_id, set())
        permitted = capability in allowed

        if not permitted:
            cls._QUARANTINED_AGENTS.add(agent_id)

        return {
            "agent_id": agent_id,
            "requested_capability": capability,
            "execution_permitted": permitted,
            "capability_violation_quarantined": not permitted,
            "runtime_security_state": "ISOLATED_SANDBOX" if not permitted else "SECURE_RING"
        }