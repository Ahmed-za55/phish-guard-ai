from typing import Dict, Any, List

class CybersecurityDigitalTwin:
    """
    نسخة افتراضية من بيئة المستخدم تحاكي تأثير قرار الحظر أو العزل قبل تطبيقه فعلياً،
    مع تفعيل التراجع التلقائي (Auto-Rollback) إذا أدى القرار إلى كسر نطاقات العمل الحرجة.
    """
    CRITICAL_INFRASTRUCTURE_DOMAINS = {"localhost", "127.0.0.1", "sovereign.internal", "kfs.edu.eg", "github.com"}

    @classmethod
    def simulate_policy_impact(cls, proposed_action: str, target_urls: List[Dict[str, Any]]) -> Dict[str, Any]:
        collateral_damage_detected = False
        affected_critical_assets = []

        for u in target_urls:
            url_str = u.get("url", "").lower()
            for crit in cls.CRITICAL_INFRASTRUCTURE_DOMAINS:
                if crit in url_str:
                    collateral_damage_detected = True
                    affected_critical_assets.append(crit)

        if collateral_damage_detected and proposed_action in {"BLOCK_AND_QUARANTINE", "ISOLATE_HOST"}:
            simulation_status = "SIMULATION_FAILED_AUTO_ROLLBACK"
            safe_fallback_action = "WARN_USER_RESTRICTED"
            rollback_triggered = True
        else:
            simulation_status = "SIMULATION_PASSED_SAFE_TO_APPLY"
            safe_fallback_action = proposed_action
            rollback_triggered = False

        return {
            "twin_simulation_status": simulation_status,
            "proposed_action_tested": proposed_action,
            "approved_post_simulation_action": safe_fallback_action,
            "auto_rollback_triggered": rollback_triggered,
            "affected_critical_assets": affected_critical_assets,
            "blast_radius_score": 0.0 if not collateral_damage_detected else 0.85
        }