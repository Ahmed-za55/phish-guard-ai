import sys
import time
import hmac
import hashlib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.frontier_expansion_v5.frontier_1_abuse_and_api import ProductAbuseAndSecureApi
from app.frontier_expansion_v5.frontier_2_data_sovereignty import DataSovereigntyAssurance
from app.frontier_expansion_v5.frontier_3_update_intelligence import SecurityUpdateIntelligence
from app.frontier_expansion_v5.frontier_4_experience_reliability import ExperienceAndReliabilityIntelligence

def test_frontier_expansion_v5_suite():
    # 1. Product Abuse Defense: اكتشاف الأتمتة المفرطة
    abuse = ProductAbuseAndSecureApi.inspect_api_abuse("1.2.3.4", 80, "python-requests/2.31", 10.0)
    assert abuse["bot_pattern_detected"] is True
    assert abuse["mitigation_action"] == "THROTTLE_AND_CHALLENGE"

    # Webhook Replay Protection
    secret = "test_secret_key"
    ts = int(time.time())
    nonce = "nonce_12345"
    sig = hmac.new(secret.encode(), f"payload_x:{nonce}:{ts}".encode(), hashlib.sha256).hexdigest()
    
    first_call = ProductAbuseAndSecureApi.verify_webhook_and_replay(secret, "payload_x", sig, nonce, ts)
    assert first_call["valid"] is True

    replay_call = ProductAbuseAndSecureApi.verify_webhook_and_replay(secret, "payload_x", sig, nonce, ts)
    assert replay_call["valid"] is False
    assert replay_call["reason"] == "REPLAY_ATTACK_DETECTED"

    # 2. Data Sovereignty: Cryptographic Erasure
    DataSovereigntyAssurance.register_tenant_key("tenant_01", "super_secret_key_bytes")
    erase_res = DataSovereigntyAssurance.execute_cryptographic_erasure("tenant_01")
    assert erase_res["key_destroyed"] is True
    assert erase_res["data_render_unrecoverable"] is True

    # PII Exposure Monitor
    pii = DataSovereigntyAssurance.monitor_sensitive_data_exposure("Payment with card number 1234 and password=secret")
    assert pii["pii_leakage_detected"] is True

    # 3. Security Update Intelligence: رصد التراجع والتراجع التلقائي
    reg_update = SecurityUpdateIntelligence.evaluate_canary_update("v5.1", 0.05, 0.01, True)
    assert reg_update["security_regression_detected"] is True
    assert reg_update["automatic_rollback_triggered"] is True

    # 4. Human-Centric & Reliability
    exp = ExperienceAndReliabilityIntelligence.generate_explainable_warning("Urgent password reset required immediately", 85.0)
    assert "Coercive urgency" in exp["human_readable_explanation"]
    assert exp["adaptive_analysis_depth"] == "DEEP_FORENSIC"

    rel = ExperienceAndReliabilityIntelligence.verify_service_resilience(["reputation_cache"])
    assert rel["graceful_degradation_active"] is True
    assert rel["core_protection_intact"] is True

    print("[VERIFIED] PHISHGUARD SOVEREIGN v5.0 FRONTIER EXPANSION Acceptance Suite PASSED 100%!")

if __name__ == "__main__":
    test_frontier_expansion_v5_suite()