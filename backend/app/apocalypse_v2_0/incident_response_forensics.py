import hashlib
import time
import json
from typing import Dict, Any, List

class IncidentForensicsAndResponse:
    """
    L5 & L6 — Incident Forensics & Autonomous Response:
    جمع الأدلة الرقمية، إنشاء تسلسل زمني للحادث (Timeline)، إدارة سلسلة الحيازة (Chain of Custody)،
    وتنفيذ إجراءات الاحتواء والتعافي مع ضوابط بشرية.
    """
    _CHAIN_OF_CUSTODY_LOG: List[Dict[str, Any]] = []

    @classmethod
    def record_evidence_chain_of_custody(cls, incident_id: str, evidence_item: str, collector: str) -> Dict[str, Any]:
        evidence_hash = hashlib.sha256(evidence_item.encode("utf-8")).hexdigest()
        seq = len(cls._CHAIN_OF_CUSTODY_LOG)
        prev_h = cls._CHAIN_OF_CUSTODY_LOG[-1]["custody_hash"] if cls._CHAIN_OF_CUSTODY_LOG else "0" * 64

        entry = {
            "sequence": seq,
            "incident_id": incident_id,
            "collector": collector,
            "evidence_sha256": evidence_hash,
            "previous_custody_hash": prev_h,
            "timestamp": int(time.time())
        }
        custody_hash = hashlib.sha256(json.dumps(entry, sort_keys=True).encode()).hexdigest()
        signed_entry = {**entry, "custody_hash": custody_hash}
        cls._CHAIN_OF_CUSTODY_LOG.append(signed_entry)
        return signed_entry

    @staticmethod
    def orchestrate_incident_response(risk_score: float, affected_assets: List[str]) -> Dict[str, Any]:
        requires_human = risk_score >= 70.0
        actions = []
        if risk_score >= 85.0:
            actions.append("ISOLATE_ENDPOINT_HOST")
            actions.append("REVOKE_USER_SESSION_TOKENS")
        elif risk_score >= 50.0:
            actions.append("STEP_UP_MFA_CHALLENGE")
            actions.append("QUARANTINE_EMAIL_INBOX")
        else:
            actions.append("LOG_AND_MONITOR")

        return {
            "incident_severity_score": risk_score,
            "affected_assets": affected_assets,
            "recommended_playbook_actions": actions,
            "human_approval_required": requires_human,
            "response_status": "PENDING_HUMAN_OPERATOR_SIGN_OFF" if requires_human else "AUTOMATED_CONTAINMENT_EXECUTED"
        }