from __future__ import annotations
import hmac
import hashlib
import json

SECRET_KEY = b"phish-guard-sovereign-attestation-key-2026"

class CryptographicAttestationCore:
    @staticmethod
    def sign_report(report_data: dict) -> str:
        # استبعاد الحقول المتداخلة أو التي قد تحتوي على مراجع دائرية لتجنب ValueError
        clean_data = {
            k: v for k, v in report_data.items() 
            if k not in ('warrant_payload', 'blockchain_audit_block', 'warrant_signature')
        }
        payload = json.dumps(clean_data, sort_keys=True, default=str).encode("utf-8")
        return hmac.new(SECRET_KEY, payload, hashlib.sha256).hexdigest()
