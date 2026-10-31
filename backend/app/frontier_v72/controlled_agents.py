from typing import Dict, Any, List

class ControlledAgentsAndCollaborativeLearning:
    """
    الطبقة الخامسة: بروتوكولات الوكلاء الموثقة (عقود الصلاحيات وحدود الموارد)
    والتعلم التعاوني المقاوم لتسميم البيانات (Byzantine-Resilient Federated Learning).
    """
    AGENT_CONTRACT = {
        "max_execution_steps": 5,
        "max_memory_mb": 256,
        "allowed_scopes": ["READ_TELEMETRY", "PROPOSE_VERDICT", "EMIT_AUDIT_LOG"],
        "forbidden_scopes": ["MUTATE_KERNEL", "DISABLE_FIREWALL", "RAW_SOCKET_EGRESS"]
    }

    @classmethod
    def enforce_verified_agent_protocol(cls, requested_scope: str, steps_taken: int) -> Dict[str, Any]:
        scope_valid = (requested_scope in cls.AGENT_CONTRACT["allowed_scopes"]) and (requested_scope not in cls.AGENT_CONTRACT["forbidden_scopes"])
        budget_valid = steps_taken <= cls.AGENT_CONTRACT["max_execution_steps"]
        contract_honored = scope_valid and budget_valid
        return {
            "agent_contract_honored": contract_honored,
            "requested_scope": requested_scope,
            "steps_used": f"{steps_taken}/{cls.AGENT_CONTRACT['max_execution_steps']}",
            "protocol_enforcement": "PERMITTED" if contract_honored else "TERMINATED_CONTRACT_VIOLATION"
        }

    @staticmethod
    def aggregate_collaborative_threat_intel(peer_risk_scores: List[float]) -> Dict[str, Any]:
        # مقاومة تسميم البيانات (Data Poisoning Defense) عبر حذف القيم المتطرفة (Trimmed Mean / Median Filtering)
        if not peer_risk_scores:
            return {"collaborative_consensus_score": 0.0, "poisoned_Updates_rejected": 0}

        sorted_scores = sorted(peer_risk_scores)
        median = sorted_scores[len(sorted_scores) // 2]
        clean_scores = [s for s in sorted_scores if abs(s - median) <= 35.0]
        poisoned_count = len(sorted_scores) - len(clean_scores)

        consensus = round(sum(clean_scores) / max(len(clean_scores), 1), 2)
        return {
            "collaborative_consensus_score": consensus,
            "participating_peers": len(peer_risk_scores),
            "poisoned_updates_rejected": poisoned_count,
            "byzantine_robust_aggregation": "TRIMMED_MEDIAN_FILTER"
        }