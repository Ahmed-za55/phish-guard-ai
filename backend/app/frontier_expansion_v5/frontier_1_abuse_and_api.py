import time
import hmac
import hashlib
from typing import Dict, Any, List

class ProductAbuseAndSecureApi:
    """
    1. Autonomous Product Abuse Defense: صد استنزاف الموارد وأتمتة الـ Bots والتلاعب بالواجهات.
    2. Secure API Ecosystem: التحقق من توقيع Webhooks ومنع Replay Attacks.
    """
    _REQUEST_NONCES = set()

    @classmethod
    def inspect_api_abuse(cls, client_ip: str, request_rate_per_min: int, user_agent: str, payload_size_kb: float) -> Dict[str, Any]:
        is_bot_pattern = any(b in user_agent.lower() for b in ["python-requests", "curl", "headless", "bot"]) and request_rate_per_min > 60
        is_resource_exhaustion = payload_size_kb > 10240.0 or request_rate_per_min > 300

        abusive = is_bot_pattern or is_resource_exhaustion
        return {
            "client_ip": client_ip,
            "bot_pattern_detected": is_bot_pattern,
            "resource_exhaustion_attempt": is_resource_exhaustion,
            "abuse_detected": abusive,
            "mitigation_action": "THROTTLE_AND_CHALLENGE" if is_bot_pattern else ("DROP_CONNECTION" if is_resource_exhaustion else "PERMIT")
        }

    @classmethod
    def verify_webhook_and_replay(cls, secret_key: str, payload: str, signature: str, nonce: str, timestamp: int) -> Dict[str, Any]:
        # حماية ضد Replay Attack (صلاحية 5 دقائق + Nonce فريد)
        current_time = int(time.time())
        if abs(current_time - timestamp) > 300:
            return {"valid": False, "reason": "TIMESTAMP_EXPIRED"}
        
        if nonce in cls._REQUEST_NONCES:
            return {"valid": False, "reason": "REPLAY_ATTACK_DETECTED"}
        
        expected_sig = hmac.new(secret_key.encode(), f"{payload}:{nonce}:{timestamp}".encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected_sig, signature):
            return {"valid": False, "reason": "INVALID_SIGNATURE"}

        cls._REQUEST_NONCES.add(nonce)
        return {"valid": True, "reason": "AUTHENTICATED_AND_NON_REPLAYED"}