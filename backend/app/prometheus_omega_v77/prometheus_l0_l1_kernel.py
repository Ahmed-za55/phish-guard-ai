import hashlib
import json
from typing import Dict, Any, Set

class PrometheusKernelAndTrust:
    """
    L0 & L1:
    - Cryptographic Trust Fabric & Hardware Trust (TPM/Secure Boot simulation)
    - Sovereign Security Kernel & Proof-Carrying Decisions (لا تنفيذ دون صلاحية، سجل يحمل الأدلة والإثباتات).
    """
    ALLOWED_ACTIONS: Set[str] = {
        "PASSIVE_OBSERVE",
        "WARN_USER_RESTRICTED",
        "STEP_UP_MFA",
        "QUARANTINE_SESSION"
    }

    @classmethod
    def evaluate_kernel_and_issue_proof(cls, proposed_action: str, agent_id: str, evidence_digest: str, model_version: str) -> Dict[str, Any]:
        violation = proposed_action not in cls.ALLOWED_ACTIONS
        permitted = not violation

        enforced = proposed_action if permitted else "WARN_USER_RESTRICTED"

        # 13: Proof-Carrying Decisions
        proof_payload = {
            "agent_id": agent_id,
            "action_enforced": enforced,
            "evidence_digest": evidence_digest,
            "model_version": model_version,
            "kernel_policy_version": "Prometheus-Kernel-v77.0"
        }
        canonical_bytes = json.dumps(proof_payload, sort_keys=True).encode("utf-8")
        decision_proof_hash = hashlib.sha256(canonical_bytes).hexdigest()

        return {
            "execution_permitted": permitted,
            "enforced_action": enforced,
            "proof_carrying_decision": {
                "decision_hash": decision_proof_hash,
                "hardware_tpm_attestation": "PCR_QUOTE_VALID_TPM2_SIMULATED",
                "proof_metadata": proof_payload
            }
        }