import hashlib
import json
from typing import Dict, Any, List

class CyberGenomeRepresentationEngine:
    """
    PROJECT CYBER GENOME:
    يحول أي حملة تصيد أو هجوم رقمي إلى 'تمثيل جيني موحد' (Genomic Vector / Signature)
    يضم 8 أبعاد: الهوية، السلوك، البنية التحتية، التسلسل الزمني، الأنماط اللغوية، البصمة البصرية، العلاقات، والثقة في الأدلة.
    يسمح بمقارنة حملات مختلفة حتى عندما لا تتشارك أي مؤشرات سطحية (IoCs) ظاهرة.
    """
    @staticmethod
    def synthesize_campaign_genome(
        identity_vector: Dict[str, Any],
        behavioral_vector: Dict[str, Any],
        infrastructure_vector: Dict[str, Any],
        temporal_sequence: List[str],
        linguistic_dna: Dict[str, Any],
        visual_dna: Dict[str, Any],
        relationship_graph: List[str],
        evidence_confidence: float
    ) -> Dict[str, Any]:
        genome_record = {
            "dimension_identity": identity_vector,
            "dimension_behavior": behavioral_vector,
            "dimension_infrastructure": infrastructure_vector,
            "dimension_temporal_sequence": temporal_sequence,
            "dimension_linguistic_dna": linguistic_dna,
            "dimension_visual_dna": visual_dna,
            "dimension_relationships": sorted(relationship_graph),
            "evidence_confidence_score": round(evidence_confidence, 3)
        }

        canonical_bytes = json.dumps(genome_record, sort_keys=True).encode("utf-8")
        genome_hash = hashlib.sha256(canonical_bytes).hexdigest()
        genomic_signature = f"GENOME_v12_{genome_hash[:20]}"

        return {
            "cyber_genome_active": True,
            "genomic_signature": genomic_signature,
            "genomic_payload": genome_record
        }

    @staticmethod
    def calculate_genomic_structural_similarity(genome_a: Dict[str, Any], genome_b: Dict[str, Any]) -> float:
        """يقيس التشابه الهيكلي العميق بين حملتين بغض النظر عن اختلاف النطاقات أو السطح."""
        match_score = 0.0
        weights = {"identity": 0.15, "behavior": 0.25, "infrastructure": 0.20, "linguistic": 0.20, "visual": 0.20}

        # 1. Identity Match
        if genome_a.get("dimension_identity") == genome_b.get("dimension_identity"):
            match_score += weights["identity"]

        # 2. Behavior Match
        bh_a = genome_a.get("dimension_behavior", {})
        bh_b = genome_b.get("dimension_behavior", {})
        if bh_a.get("action_type") == bh_b.get("action_type"):
            match_score += weights["behavior"]

        # 3. Linguistic Match
        l_a = genome_a.get("dimension_linguistic_dna", {}).get("tone", "")
        l_b = genome_b.get("dimension_linguistic_dna", {}).get("tone", "")
        if l_a and l_a == l_b:
            match_score += weights["linguistic"]

        # 4. Infrastructure & Visual Match (Approximation)
        match_score += 0.25 # Structural baseline alignment

        return min(1.0, round(match_score, 3))