from typing import Dict, Any, List

class IdentityCompromiseRecoveryEngine:
    """
    1. Identity Compromise Prevention & Recovery:
    - يكتشف إعادة استخدام جلسات الـ Session Cookies وتغييرات الـ MFA المشبوهة.
    - يحلل تطبيقات الـ OAuth المريبة وصلاحياتها الواسعة.
    - يرصد إنشاء قواعد إعادة توجيه البريد المخفية (Hidden Forwarding Rules).
    """
    @staticmethod
    def inspect_post_phish_identity_signals(
        session_cookie_anomaly: bool,
        oauth_requested_scopes: List[str],
        inbox_forwarding_rule_created: bool,
        mfa_device_changed: bool
    ) -> Dict[str, Any]:
        dangerous_oauth_scopes = {"mail.readwrite", "files.readwrite.all", "offline_access", "full_access"}
        risky_scopes_found = [s for s in oauth_requested_scopes if s.lower() in dangerous_oauth_scopes]

        account_compromised = session_cookie_anomaly or inbox_forwarding_rule_created or (len(risky_scopes_found) >= 2)

        remediation_actions = []
        if session_cookie_anomaly:
            remediation_actions.append("REVOKE_ALL_ACTIVE_SESSIONS")
        if inbox_forwarding_rule_created:
            remediation_actions.append("DELETE_MALICIOUS_INBOX_RULES")
        if risky_scopes_found:
            remediation_actions.append("REVOKE_SUSPICIOUS_OAUTH_GRANTS")
        if mfa_device_changed:
            remediation_actions.append("ENFORCE_MFA_STEP_UP_CHALLENGE")

        return {
            "identity_protection_tier": "POST_COMPROMISE_RECOVERY",
            "account_compromise_detected": account_compromised,
            "session_hijacking_anomaly": session_cookie_anomaly,
            "dangerous_oauth_grants": risky_scopes_found,
            "hidden_forwarding_rule_detected": inbox_forwarding_rule_created,
            "automated_remediation_actions": remediation_actions
        }