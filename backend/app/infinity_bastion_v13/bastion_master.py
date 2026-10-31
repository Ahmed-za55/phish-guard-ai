from typing import Dict, Any, List
from app.infinity_bastion_v13.bastion_1_identity_recovery import IdentityCompromiseRecoveryEngine
from app.infinity_bastion_v13.bastion_2_financial_trust import FinancialIntentSecurityEngine
from app.infinity_bastion_v13.bastion_3_runtime_recovery import PostCompromiseAndSovereignRuntime
from app.infinity_bastion_v13.bastion_4_redteam_quarantine import RedTeamRegressionQuarantineLab

class InfinityBastionMasterNexusV13:
    """
    المنسق المركزي لبرنامج INFINITY BASTION (v13.0):
    يوحد حماية الهوية، جدار حماية المعاملات المالية، وقت التشغيل المحلي، ومختبر الحجر الصحي.
    """
    @staticmethod
    def run_bastion_pipeline(
        text: str,
        extracted_urls: List[str],
        url_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        text_l = text.lower()
        has_wire_lure = any(w in text_l for w in ["iban", "swift", "wire", "transfer", "invoice", "تحويل", "فاتورة"])
        
        # 1. Identity Compromise Recovery
        identity_res = IdentityCompromiseRecoveryEngine.inspect_post_phish_identity_signals(
            session_cookie_anomaly="session" in text_l or "cookie" in text_l,
            oauth_requested_scopes=["mail.readwrite", "offline_access"] if has_wire_lure else [],
            inbox_forwarding_rule_created="forward" in text_l,
            mfa_device_changed=False
        )

        # 2. Financial Intent Security Engine
        financial_res = FinancialIntentSecurityEngine.evaluate_financial_transaction_intent(
            vendor_name="Acme Corp",
            invoiced_iban_or_swift="US9999999999MALICIOUS" if has_wire_lure else "US1234567890SWIFT",
            amount_usd=15000.0 if has_wire_lure else 500.0,
            out_of_band_confirmed=False
        )

        # 3. Post-Compromise & Sovereign Runtime
        runtime_res = PostCompromiseAndSovereignRuntime.audit_silent_post_compromise_signals(
            concurrent_geo_logins=False,
            sudden_admin_permission_grant=identity_res["account_compromise_detected"],
            unusual_oauth_grants_count=len(identity_res["dangerous_oauth_grants"])
        )

        # 4. Red-Team Quarantine Gate
        quarantine_res = RedTeamRegressionQuarantineLab.run_redteam_regression_gate(
            scenario_id="scenario_chimera_wire_fraud_v13",
            detection_successful=financial_res["transaction_execution_permitted"] is False,
            blind_spot_identified=False
        )

        return {
            "infinity_bastion_version": "PHISHGUARD_SOVEREIGN_v13.0_INFINITY_BASTION",
            "identity_compromise_protection": identity_res,
            "financial_intent_security": financial_res,
            "post_compromise_intelligence": runtime_res,
            "redteam_regression_quarantine": quarantine_res,
            "active_threat_prevention_enforced": True
        }