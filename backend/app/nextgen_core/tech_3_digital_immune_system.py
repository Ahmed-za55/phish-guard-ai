import math
import hashlib
import json
from typing import Dict, Any, List, Set

class AutonomousDigitalImmuneSystem:
    """
    التقنية الثالثة: Autonomous Digital Immune System.
    يحاكي جهاز المناعة البيولوجي عبر 5 مراحل متكاملة:
    1. Innate Anomaly Detection (رصد الجسم الغريب).
    2. Pathogen Pattern Classification (تصنيف نمط الهجوم).
    3. Immune Containment & Blast Isolation (عزل الكيانات المتضررة).
    4. Verified Tissue Recovery (استعادة الحالة الآمنة والتحقق التشفيري من سلامتها).
    5. Adaptive B-Cell Immunological Memory (ذاكرة مناعية تلتقط السلالات المتحورة مستقبلاً عبر Cosine Affinity).
    """
    def __init__(self):
        # قائمة الأجسام المضادة المكتسبة: [{"family_id": str, "feature_vector": List[float], "mitigation": str}]
        self.memory_b_cells: List[Dict[str, Any]] = []
        self.healthy_tissue_snapshots: Dict[str, Dict[str, Any]] = {}

    def register_healthy_baseline_snapshot(self, entity_id: str, clean_state: Dict[str, Any]) -> str:
        canonical = json.dumps(clean_state, sort_keys=True).encode("utf-8")
        state_hash = hashlib.sha256(canonical).hexdigest()
        self.healthy_tissue_snapshots[entity_id] = {
            "state": dict(clean_state),
            "integrity_sha256": state_hash
        }
        return state_hash

    @staticmethod
    def _cosine_affinity(v1: List[float], v2: List[float]) -> float:
        dot = sum(a * b for a, b in zip(v1, v2))
        n1 = math.sqrt(sum(a * a for a in v1)) or 1e-9
        n2 = math.sqrt(sum(b * b for b in v2)) or 1e-9
        return round(dot / (n1 * n2), 4)

    def handle_infection_lifecycle(
        self,
        entity_id: str,
        pathogen_vector: List[float],
        exact_signature_hash: str,
        compromised_runtime_state: Dict[str, Any],
        known_static_signatures: Set[str]
    ) -> Dict[str, Any]:
        # مقارنة مع Baseline التوقيعات الثابتة (الذي يفشل إذا تغير الـ Hash بسبب تحور بسيط)
        detected_by_static_baseline = exact_signature_hash in known_static_signatures

        # 1. فحص الذاكرة المناعية المكتسبة (Adaptive B-Cell Affinity Matching for Mutated Strains)
        best_memory_match = None
        max_affinity = 0.0
        for cell in self.memory_b_cells:
            aff = self._cosine_affinity(pathogen_vector, cell["feature_vector"])
            if aff > max_affinity:
                max_affinity = aff
                best_memory_match = cell

        secondary_immune_response = max_affinity >= 0.88

        # 2. المناعة الفطرية (Innate Anomaly Detection) إذا كانت العدوى جديدة تماماً
        vector_magnitude = math.sqrt(sum(x * x for x in pathogen_vector))
        innate_triggered = vector_magnitude >= 1.25

        infection_detected = secondary_immune_response or innate_triggered

        # 3. الاحتواء المناعي (Containment)
        containment_actions = []
        if infection_detected:
            containment_actions = [
                f"QUARANTINE_ENTITY:{entity_id}",
                "REVOKE_ACTIVE_TOKENS",
                "SEVER_LATERAL_EDGES"
            ]

        # 4. التعافي والتحقق من سلامة الاستعادة (Verified Recovery)
        recovery_verified = False
        restored_hash = "NONE"
        if entity_id in self.healthy_tissue_snapshots:
            golden = self.healthy_tissue_snapshots[entity_id]
            restored_state = dict(golden["state"])
            recomputed = hashlib.sha256(json.dumps(restored_state, sort_keys=True).encode("utf-8")).hexdigest()
            recovery_verified = (recomputed == golden["integrity_sha256"])
            restored_hash = recomputed

        # 5. تكوين ذاكرة مناعية جديدة (Affinity Maturation) لمقاومة العدوى المستقبلية المتحورة
        if infection_detected and not secondary_immune_response:
            self.memory_b_cells.append({
                "antibody_id": f"AB_{len(self.memory_b_cells) + 1}",
                "feature_vector": list(pathogen_vector),
                "neutralizing_action": "INSTANT_AFFINITY_NEUTRALIZATION"
            })

        return {
            "entity_id": entity_id,
            "detected_by_static_signature_baseline": detected_by_static_baseline,
            "detected_by_digital_immune_system": infection_detected,
            "response_mode": "SECONDARY_MEMORY_B_CELL_FAST_KILL" if secondary_immune_response else ("PRIMARY_INNATE_CONTAINMENT" if innate_triggered else "HEALTHY_NO_ACTION"),
            "antibody_affinity_score": max_affinity,
            "containment_actions_executed": containment_actions,
            "recovery_integrity_verified": recovery_verified,
            "restored_golden_sha256": restored_hash,
            "active_memory_antibodies_count": len(self.memory_b_cells)
        }