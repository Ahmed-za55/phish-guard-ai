from typing import Dict, Any, List

class TitanCognitiveIntelligencePlane:
    """
    الطبقة الثانية: النواة المعرفية (Sovereign Cognitive Defense Core).
    تتضمن Threat Memory، Context Engine، Reasoning، Uncertainty، Planning، وSafety Kernel.
    """
    _THREAT_MEMORY: List[Dict[str, Any]] = []

    @classmethod
    def execute_cognitive_reasoning(cls, text: str, entropy_val: float) -> Dict[str, Any]:
        # 1. Threat Memory & Context Engine
        context_tags = []
        if "login" in text.lower() or "password" in text.lower():
            context_tags.append("CREDENTIAL_HARVESTING_CONTEXT")
        if "urgent" in text.lower() or "immediate" in text.lower():
            context_tags.append("COERCIVE_URGENCY_CONTEXT")

        # 2. Uncertainty Engine
        epistemic_uncertainty = 0.55 if len(context_tags) == 0 or entropy_val >= 4.8 else 0.15
        requires_human_review = epistemic_uncertainty >= 0.40

        # 3. Reasoning & Planning Engine
        proposed_plan = "QUARANTINE_SESSION" if len(context_tags) >= 2 else "WARN_USER"

        cls._THREAT_MEMORY.append({"context": context_tags, "plan": proposed_plan})

        return {
            "cognitive_context_tags": context_tags,
            "epistemic_uncertainty_score": epistemic_uncertainty,
            "requires_human_review": requires_human_review,
            "cognitive_defense_plan": proposed_plan,
            "threat_memory_total_entries": len(cls._THREAT_MEMORY)
        }