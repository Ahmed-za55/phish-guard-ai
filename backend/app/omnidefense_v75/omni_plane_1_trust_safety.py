import hashlib
from typing import Dict, Any, Set

class OmniTrustAndSafetyPlane:
    """
    الطبقة الأولى: الثقة المدعومة بالعتاد (TPM/Remote Attestation)، نواة السلامة المستقلة،
    والاستجابة المقيدة رياضياً (Formally Constrained Response) التي تمنع الوكيل من تجاوز صلاحياته.
    """
    ALLOWED_ACTIONS: Set[str] = {
        "PASSIVE_OBSERVE",
        "WARN_USER_RESTRICTED",
        "STEP_UP_MFA_CHALLENGE",
        "QUARANTINE_SESSION_SANDBOX",
        "HOLD_FOR_HUMAN_REVIEW"
    }
    FORBIDDEN_ACTIONS: Set[str] = {
        "BYPASS_SAFETY_KERNEL",
        "DISABLE_AUDIT_LOGS",
        "TERMINATE_CORE_INFRASTRUCTURE",
        "GRANT_UNRESTRICTED_PRIVILEGES"
    }

    @classmethod
    def evaluate_runtime_safety_kernel(cls, proposed_action: str, agent_compromised: bool, human_signoff: bool = False) -> Dict[str, Any]:
        violation = (proposed_action in cls.FORBIDDEN_ACTIONS) or (proposed_action not in cls.ALLOWED_ACTIONS)

        if agent_compromised or violation:
            enforced = "WARN_USER_RESTRICTED"
            permitted = False
        elif proposed_action in {"QUARANTINE_SESSION_SANDBOX"} and not human_signoff:
            enforced = "HOLD_FOR_HUMAN_REVIEW"
            permitted = False
        else:
            enforced = proposed_action
            permitted = True

        return {
            "proposed_action": proposed_action,
            "enforced_action": enforced,
            "execution_permitted": permitted,
            "formal_constraint_verified": enforced in cls.ALLOWED_ACTIONS,
            "hardware_tpm_attestation_status": "TPM_PCR_QUOTE_VALID_SIMULATED"
        }