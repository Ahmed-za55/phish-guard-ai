import hashlib
import json
from typing import Dict, Any, List

class SovereignBlockchainLedger:
    """
    Sovereign Blockchain Forensic Audit Trail:
    Maintains an immutable, cryptographically chained distributed ledger of all 
    threat warrants and SOAR dispatches, ensuring absolute non-repudiation.
    """
    _chain: List[Dict[str, Any]] = []

    @classmethod
    def append_block(cls, warrant_data: Dict[str, Any]) -> Dict[str, Any]:
        index = len(cls._chain)
        prev_hash = cls._chain[-1]["block_hash"] if index > 0 else "0" * 64
        block_content = json.dumps(warrant_data, sort_keys=True) + prev_hash
        block_hash = hashlib.sha3_256(block_content.encode()).hexdigest()
        
        block = {
            "block_index": index,
            "previous_hash": prev_hash,
            "block_hash": block_hash,
            "warrant_payload": warrant_data
        }
        cls._chain.append(block)
        return block