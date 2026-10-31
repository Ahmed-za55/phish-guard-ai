import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.infinity_bastion_v13.bastion_1_identity_recovery import IdentityCompromiseRecoveryEngine
from app.infinity_bastion_v13.bastion_2_financial_trust import FinancialIntentSecurityEngine
from app.infinity_bastion_v13.bastion_3_runtime_recovery import PostCompromiseAndSovereignRuntime
from app.infinity_bastion_v13.bastion_4_redteam_quarantine import RedTeamRegressionQuarantineLab
from app.infinity_bastion_v13.bastion_master import InfinityBastionMasterNexusV13

def test_infinity_bastion_v13_suite():
    # 1. Identity Compromise Recovery: اكتشاف سرقة الجلسة و OAuth المريب وقواعد إعادة التوجيه
    id_res = IdentityCompromiseRecoveryEngine.inspect_post_phish_identity_signals(
        session_cookie_anomaly=True,
        oauth_requested_scopes=["mail.readwrite", "offline_access"],
        inbox_forwarding_rule_created=True,
        mfa_device_changed=False
    )
    assert id_res["account_compromise_detected"] is True
    assert "REVOKE_ALL_ACTIVE_SESSIONS" in id_res["automated_remediation_actions"]
    assert "DELETE_MALICIOUS_INBOX_RULES" in id_res["automated_remediation_actions"]

    # 2. Financial Intent Security: كشف تغيير حساب التحويل البنكي (BEC Fraud) وفرض IOTP
    fin_res = FinancialIntentSecurityEngine.evaluate_financial_transaction_intent(
        vendor_name="Acme Corp",
        invoiced_iban_or_swift="US9999999999MALICIOUS", # مخالف للحساب المعتمد US1234567890SWIFT
        amount_usd=12000.0,
        out_of_band_confirmed=False
    )
    assert fin_res["beneficiary_account_mismatch"] is True
    assert fin_res["independent_trust_confirmation_required"] is True
    assert fin_res["transaction_execution_permitted"] is False
    assert fin_res["enforced_action"] == "BLOCK_AND_REQUIRE_OUT_OF_BAND_VERIFICATION"

    # 3. Sovereign Runtime & Offline Mode: التشغيل المحلي والتحقق
    run_res = PostCompromiseAndSovereignRuntime.execute_offline_sovereign_analysis("sha256_mock", True)
    assert run_res["runtime_mode"] == "AIR_GAPPED_OFFLINE_SOVEREIGN"
    assert run_res["offline_signature_valid"] is True

    # 4. Red-Team Regression Quarantine Lab
    lab_res = RedTeamRegressionQuarantineLab.run_redteam_regression_gate("test_wire_fraud_01", True, False)
    assert lab_res["regression_quarantine_passed"] is True
    assert lab_res["promotion_gate_verdict"] == "CERTIFIED_FOR_PRODUCTION"

    # 5. Full v13 Pipeline Integration
    full = InfinityBastionMasterNexusV13.run_bastion_pipeline(
        text="Please wire invoice payment to our new IBAN account US9999999999MALICIOUS immediately. Review rules.",
        extracted_urls=[],
        url_results=[]
    )
    assert full["active_threat_prevention_enforced"] is True
    assert full["financial_intent_security"]["transaction_execution_permitted"] is False

    print("[VERIFIED] PHISHGUARD SOVEREIGN v13.0 INFINITY BASTION Acceptance Suite PASSED 100%!")

if __name__ == "__main__":
    test_infinity_bastion_v13_suite()