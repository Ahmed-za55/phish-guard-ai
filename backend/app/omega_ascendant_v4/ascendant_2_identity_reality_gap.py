from typing import Dict, Any, List

class MachineIdentityAndRealityGap:
    """
    1. Machine Identity Defense: حماية Service Accounts وهوية وكلاء الذكاء الاصطناعي.
    2. Cyber Reality Gap Detector: كشف الفجوة بين التصميم المعماري والواقع التشغيلي الفعلي.
    """
    @staticmethod
    def inspect_machine_identity(token_issuer: str, caller_service: str, requested_scope: List[str], allowed_scopes: List[str]) -> Dict[str, Any]:
        unauthorized_scope = [s for s in requested_scope if s not in allowed_scopes]
        is_impersonation_suspected = len(unauthorized_scope) > 0 or "root" in requested_scope

        return {
            "caller_service": caller_service,
            "impersonation_suspected": is_impersonation_suspected,
            "unauthorized_scopes_attempted": unauthorized_scope,
            "token_validity": not is_impersonation_suspected,
            "enforced_action": "REVOKE_TOKEN_IMMEDIATELY" if is_impersonation_suspected else "ALLOW_SCOPED_ACCESS"
        }

    @staticmethod
    def detect_reality_gap(documented_services: List[str], active_runtime_services: List[str], granted_admin_services: List[str]) -> Dict[str, Any]:
        shadow_services = [s for s in active_runtime_services if s not in documented_services]
        excessive_privilege_services = [s for s in granted_admin_services if s not in documented_services or "guest" in s]

        reality_gap_present = len(shadow_services) > 0 or len(excessive_privilege_services) > 0

        return {
            "reality_gap_detected": reality_gap_present,
            "shadow_undocumented_services": shadow_services,
            "excessive_privilege_anomalies": excessive_privilege_services,
            "visibility_health_rating": "CRITICAL_DRIFT" if reality_gap_present else "SYNCHRONIZED"
        }