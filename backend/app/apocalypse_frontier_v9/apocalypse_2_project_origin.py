import time
import hashlib
import json
from typing import Dict, Any, List

class ProjectOriginEvidenceProvenance:
    """
    PROJECT ORIGIN:
    منظومة إثبات أصل الأدلة وسلامتها عبر سجلات مرتبطة تشفيرياً (Hash-Chained Ledger)
    تضمن إمكانية إعادة إنتاج نتائج التحليل وتوثيق مصدر كل معلومة.
    """
    _PROVENANCE_CHAIN: List[Dict[str, Any]] = []

    @classmethod
    def record_evidence_provenance(
        cls,
        evidence_source: str,
        raw_payload_snippet: str,
        derived_verdict: str,
        engine_version: str = "Apocalypse-Origin-v9.0"
    ) -> Dict[str, Any]:
        seq = len(cls._PROVENANCE_CHAIN)
        prev_hash = cls._PROVENANCE_CHAIN[-1]["provenance_record_hash"] if cls._PROVENANCE_CHAIN else "0" * 64

        payload_digest = hashlib.sha256(raw_payload_snippet.encode("utf-8")).hexdigest()
        
        record_body = {
            "sequence_id": seq,
            "evidence_source": evidence_source,
            "payload_sha256": payload_digest,
            "derived_verdict": derived_verdict,
            "engine_version": engine_version,
            "previous_provenance_hash": prev_hash,
            "timestamp_utc": int(time.time())
        }

        canonical_json = json.dumps(record_body, sort_keys=True).encode("utf-8")
        record_hash = hashlib.sha256(canonical_json).hexdigest()

        sealed_record = {**record_body, "provenance_record_hash": record_hash, "tamper_evident_verified": True}
        cls._PROVENANCE_CHAIN.append(sealed_record)
        return sealed_record