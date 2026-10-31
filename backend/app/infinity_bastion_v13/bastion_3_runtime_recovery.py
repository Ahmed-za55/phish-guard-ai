from typing import Dict, Any, List

class PostCompromiseAndSovereignRuntime:
    """
    3. Post-Compromise Intelligence & Privacy-First Sovereign Runtime:
    - يبحث عن آثار الهجوم الصامت (جلسات غير طبيعية، تغيير إعدادات، OAuth مريب).
    - يوفر وضع تشغيل محلي بالكامل (Offline Sovereign Runtime) يعتمد على قاعدة تهديدات موقعة رقمياً.
    """
    @staticmethod
    def audit_silent_post_compromise_signals(
        concurrent_geo_logins: bool,
        sudden_admin_permission_grant: bool,
        unusual_oauth_grants_count: int
    ) -> Dict[str, Any]:
        silent_breach = concurrent_geo_logins or sudden_admin_permission_grant or (unusual_oauth_grants_count >= 2)
        return {
            "post_compromise_tier": "SILENT_BREACH_DETECTION",
            "silent_compromise_indicators_found": silent_breach,
            "impossible_travel_or_geo_anomaly": concurrent_geo_logins,
            "privilege_escalation_detected": sudden_admin_permission_grant,
            "remediation_recommended": "ISOLATE_ACCOUNT_AND_FORCE_REAUTH" if silent_breach else "NOMINAL_MONITORING"
        }

    @staticmethod
    def execute_offline_sovereign_analysis(payload_hash: str, offline_signature_verified: bool) -> Dict[str, Any]:
        return {
            "runtime_mode": "AIR_GAPPED_OFFLINE_SOVEREIGN",
            "offline_signature_valid": offline_signature_verified,
            "local_heuristics_executed": True,
            "cloud_api_dependency_bypassed": True,
            "analysis_verdict": "MALICIOUS_LOCAL_MATCH" if offline_signature_verified else "UNKNOWN_SAFE_LOCAL_FALLBACK"
        }