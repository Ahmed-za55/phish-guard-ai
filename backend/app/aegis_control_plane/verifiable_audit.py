import hashlib
import json
from typing import Dict, Any, List

class VerifiableExecutionLedger:
    """
    سجل أحداث قابل للتحقق الجنائي وإعادة التشغيل (Deterministic Replay):
    يربط تجزئة المدخلات + إصدار السياسة + الأدلة + القرار النهائي في سلسلة غير قابلة للتلاعب.
    """
    _LEDGER_CHAIN: List[Dict[str, Any]] = []

    @classmethod
    def record_verifiable_decision(cls, input_text: str, evidence_decision: Dict[str, Any], control_plane_decision: Dict[str, Any]) -> Dict[str, Any]:
        prev_hash = cls._LEDGER_CHAIN[-1]["entry_hash"] if cls._LEDGER_CHAIN else "0" * 64
        input_digest = hashlib.sha256(input_text.encode("utf-8")).hexdigest()

        deterministic_state = {
            "sequence_index": len(cls._LEDGER_CHAIN),
            "previous_entry_hash": prev_hash,
            "input_sha256": input_digest,
            "model_version": evidence_decision["version_metadata"]["model_version"],
            "policy_version": evidence_decision["version_metadata"]["policy_version"],
            "hard_facts_count": len(evidence_decision["forensic_separation"]["hard_cryptographic_and_structural_facts"]),
            "recommended_verdict": evidence_decision["recommended_verdict"],
            "enforced_action": control_plane_decision["enforced_action"],
            "execution_permitted": control_plane_decision["execution_permitted"]
        }

        serialized_state = json.dumps(deterministic_state, sort_keys=True)
        entry_hash = hashlib.sha256(serialized_state.encode("utf-8")).hexdigest()

        record = {
            **deterministic_state,
            "entry_hash": entry_hash,
            "replay_verifiable": True
        }
        cls._LEDGER_CHAIN.append(record)
        return record

    @classmethod
    def verify_chain_integrity(cls) -> bool:
        for i in range(1, len(cls._LEDGER_CHAIN)):
            if cls._LEDGER_CHAIN[i]["previous_entry_hash"] != cls._LEDGER_CHAIN[i - 1]["entry_hash"]:
                return False
        return True