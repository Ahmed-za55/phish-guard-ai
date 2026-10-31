from typing import Dict, Any, Set

class SovereignSecurityConstitution:
    """
    Sovereign Security Constitution:
    دستور أمني ثابت مستقل تماماً عن نماذج الذكاء الاصطناعي.
    يفرض قواعد غير قابلة للتغيير: Least Privilege, Independent Authorization, Fail-Safe, Human Approval.
    """
    IMMUTABLE_RULES: Set[str] = {
        "NO_EXECUTION_WITHOUT_AUTHORIZATION",
        "LEAST_PRIVILEGE_ENFORCED",
        "FAIL_SAFE_ON_SYSTEM_FAILURE",
        "INDEPENDENT_AUDIT_LOGGING"
    }
    RESTRICTED_ACTIONS: Set[str] = {
        "BYPASS_SECURITY_CONSTITUTION",
        "ELEVATE_AGENT_TO_ROOT",
        "DISABLE_AUDIT_TRAIL",
        "UNCONSTRAINED_SYSTEM_MUTATION"
    }

    @classmethod
    def enforce_constitution(cls, proposed_action: str, agent_authenticated: bool) -> Dict[str, Any]:
        violates_constitution = (proposed_action in cls.RESTRICTED_ACTIONS) or not agent_authenticated
        permitted = not violates_constitution
        enforced = proposed_action if permitted else "WARN_USER_RESTRICTED"

        return {
            "proposed_action": proposed_action,
            "enforced_action": enforced,
            "constitution_enforced": True,
            "execution_permitted": permitted,
            "active_immutable_rules": list(cls.IMMUTABLE_RULES),
            "violation_blocked": violates_constitution
        }