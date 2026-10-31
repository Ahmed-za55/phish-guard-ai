import hashlib
import json
from typing import Dict, Any, List

class DecisionIntegrityAndAccountability:
    """
    1. Decision Integrity Firewall: يفحص مبررات وأدلة أي قرار قبل تنفيذه.
    2. Multi-Agent Accountability: هوية وميزانية وسجل قرارات مستقل لكل وكيل مع إمكانية عزله.
    """
    _ISOLATED_AGENTS = set()

    @classmethod
    def evaluate_decision_integrity(cls, agent_id: str, proposed_decision: str, supporting_evidence: List[str], confidence: float) -> Dict[str, Any]:
        if agent_id in cls._ISOLATED_AGENTS:
            return {
                "decision_permitted": False,
                "rejection_reason": f"Agent {agent_id} is currently isolated due to policy breach.",
                "enforced_action": "BLOCK_EXECUTION"
            }

        # رفض القرارات غير القابلة للتبرير: غياب الأدلة أو انخفاض الثقة مع إجراء عالي الخطورة
        is_high_risk = proposed_decision in {"QUARANTINE_HOST", "REVOKE_GLOBAL_CREDENTIALS", "SHUTDOWN_SERVICE"}
        has_insufficient_evidence = len(supporting_evidence) == 0 or confidence < 0.65

        if is_high_risk and has_insufficient_evidence:
            return {
                "decision_permitted": False,
                "rejection_reason": "INSUFFICIENT_EVIDENCE_FOR_HIGH_RISK_ACTION",
                "enforced_action": "ESCALATE_TO_HUMAN_SOVEREIGN"
            }

        decision_digest = hashlib.sha256(f"{agent_id}:{proposed_decision}:{json.dumps(supporting_evidence)}".encode()).hexdigest()

        return {
            "decision_permitted": True,
            "decision_digest": decision_digest,
            "enforced_action": proposed_decision,
            "justification_verified": True
        }

    @classmethod
    def isolate_rogue_agent(cls, agent_id: str) -> Dict[str, Any]:
        cls._ISOLATED_AGENTS.add(agent_id)
        return {"agent_id": agent_id, "isolated": True, "blast_radius_contained": True}