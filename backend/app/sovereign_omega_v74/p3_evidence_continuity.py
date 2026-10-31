import hashlib
import hmac
import json
from typing import Dict, Any, List

class CryptographicEvidenceContinuityLedger:
    """
    P3 (التطوير 8): يحافظ على سلامة أدلة الحوادث من لحظة جمعها حتى المراجعة الجنائية،
    مع توقيع التقارير وإثبات إصدارات المحللات وكشف أي حذف أو إعادة ترتيب للسجلات.
    """
    _SIGNING_SECRET = b"PHISHGUARD_OMEGA_V74_FORENSIC_CONTINUITY_KEY"
    _EVIDENCE_CHAIN: List[Dict[str, Any]] = []
    _ANALYZER_VERSIONS = {
        "immune_neuro_symbolic": "v74.1.0",
        "browser_behavior_engine": "v74.2.0",
        "identity_defense_engine": "v74.1.5"
    }

    @classmethod
    def append_signed_forensic_record(cls, payload_sha256: str, verdict: str, evidence_list: List[str]) -> Dict[str, Any]:
        seq_no = len(cls._EVIDENCE_CHAIN)
        prev_hash = cls._EVIDENCE_CHAIN[-1]["record_hash"] if cls._EVIDENCE_CHAIN else "0" * 64

        body = {
            "sequence_number": seq_no,
            "previous_record_hash": prev_hash,
            "payload_sha256": payload_sha256,
            "verdict": verdict,
            "evidence_digest": hashlib.sha256("|".join(sorted(evidence_list)).encode("utf-8")).hexdigest(),
            "analyzer_versions": cls._ANALYZER_VERSIONS
        }
        canonical = json.dumps(body, sort_keys=True).encode("utf-8")
        record_hash = hashlib.sha256(canonical).hexdigest()
        hmac_sig = hmac.new(cls._SIGNING_SECRET, canonical, hashlib.sha256).hexdigest()

        signed_record = {
            **body,
            "record_hash": record_hash,
            "hmac_signature": hmac_sig
        }
        cls._EVIDENCE_CHAIN.append(signed_record)
        return signed_record

    @classmethod
    def audit_chain_for_deletion_or_reordering(cls, external_chain_view: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        chain = external_chain_view if external_chain_view is not None else cls._EVIDENCE_CHAIN
        for idx, rec in enumerate(chain):
            # كشف الحذف أو إعادة الترتيب عبر فحص رقم التسلسل والهاش السابق
            if rec.get("sequence_number") != idx:
                return {"continuity_verified": False, "tamper_type": "RECORD_DELETION_OR_REORDERING_DETECTED", "failed_at_index": idx}
            expected_prev = "0" * 64 if idx == 0 else chain[idx - 1].get("record_hash")
            if rec.get("previous_record_hash") != expected_prev:
                return {"continuity_verified": False, "tamper_type": "HASH_LINK_BROKEN", "failed_at_index": idx}

        return {
            "continuity_verified": True,
            "tamper_type": "NONE",
            "verified_records_count": len(chain)
        }