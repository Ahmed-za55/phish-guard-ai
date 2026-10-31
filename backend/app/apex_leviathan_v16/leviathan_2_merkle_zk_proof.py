import hashlib
import hmac
from typing import Dict, Any, List

class ZeroKnowledgeMerkleAuditEngine:
    """
    2. PROJECT MERKLE-ZK:
    يبني شجرة ميركل ثنائية كاملة (Cryptographic Binary Merkle Tree) مع التزامات معمّاة
    (Blinded Commitments) بحيث يستطيع المدقق الخارجي التحقق رياضياً من أن دليلاً معيناً
    كان جزءاً من القرار الأمني في وقت محدد دون كشف البيانات السرية في باقي الأوراق.
    """
    @staticmethod
    def _hash_leaf(data: str, blinding_nonce: str) -> str:
        return hashlib.sha256(f"LEAF:{blinding_nonce}:{data}".encode("utf-8")).hexdigest()

    @staticmethod
    def _hash_pair(left: str, right: str) -> str:
        return hashlib.sha256(f"NODE:{left}:{right}".encode("utf-8")).hexdigest()

    @classmethod
    def build_tree_and_generate_zk_proof(
        cls,
        evidence_leaves: List[str],
        target_leaf_index: int = 0,
        master_blinding_seed: str = "LEVIATHAN_ZK_SEED_2026"
    ) -> Dict[str, Any]:
        if not evidence_leaves:
            evidence_leaves = ["EMPTY_EVIDENCE_LEAF"]

        # مضاعفة القائمة لتكون قوة للعدد 2 أو عدد زوجي متوازن
        leaves = list(evidence_leaves)
        while len(leaves) < 4 or (len(leaves) & (len(leaves) - 1)) != 0:
            leaves.append(leaves[-1])

        # توليد Nonce تعمية مستقل لكل ورقة لحماية الخصوصية (Zero-Knowledge Blinding)
        nonces = [
            hmac.new(master_blinding_seed.encode("utf-8"), f"slot_{i}".encode("utf-8"), hashlib.sha256).hexdigest()[:24]
            for i in range(len(leaves))
        ]
        current_level = [cls._hash_leaf(leaves[i], nonces[i]) for i in range(len(leaves))]
        leaf_commitments = list(current_level)

        audit_path = []
        idx = target_leaf_index

        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                right = current_level[i + 1]
                if i == idx or i + 1 == idx:
                    if idx % 2 == 0:
                        audit_path.append({"position": "RIGHT", "sibling_hash": right})
                    else:
                        audit_path.append({"position": "LEFT", "sibling_hash": left})
                next_level.append(cls._hash_pair(left, right))
            idx //= 2
            current_level = next_level

        merkle_root = current_level[0]

        return {
            "merkle_root_hash": merkle_root,
            "total_padded_leaves": len(leaves),
            "target_leaf_index": target_leaf_index,
            "blinded_leaf_commitment": leaf_commitments[target_leaf_index],
            "target_blinding_nonce": nonces[target_leaf_index],
            "zk_inclusion_audit_path": audit_path
        }

    @classmethod
    def verify_zk_inclusion_proof(
        cls,
        raw_leaf_value: str,
        blinding_nonce: str,
        audit_path: List[Dict[str, str]],
        expected_merkle_root: str
    ) -> bool:
        """يتحقق رياضياً من انتماء الدليل إلى جذر الشجرة دون معرفة أي ورقة أخرى."""
        computed_hash = cls._hash_leaf(raw_leaf_value, blinding_nonce)
        for step in audit_path:
            if step["position"] == "RIGHT":
                computed_hash = cls._hash_pair(computed_hash, step["sibling_hash"])
            else:
                computed_hash = cls._hash_pair(step["sibling_hash"], computed_hash)
        return hmac.compare_digest(computed_hash, expected_merkle_root)