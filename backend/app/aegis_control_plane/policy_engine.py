from typing import Dict, Any

class AegisSovereignControlPlane:
    """
    الطبقة المستقلة الحاكمة (AEGIS Control Plane):
    تفصل بين اقتراح الذكاء الاصطناعي والتنفيذ الفعلي. تمنع أي نموذج مخترق من تجاوز
    الصلاحيات أو تعديل السياسات، وتفرض موافقة بشرية للعمليات عالية التأثير.
    """
    _KILL_SWITCH_ACTIVE = False
    _IMMUTABLE_ALLOWED_ACTIONS = {
        "ALLOW_MONITORED": {"max_privilege": "READ_ONLY", "requires_human_approval": False},
        "WARN_USER_RESTRICTED": {"max_privilege": "UI_BANNER_INJECTION", "requires_human_approval": False},
        "BLOCK_AND_QUARANTINE": {"max_privilege": "DOM_QUARANTINE_ONLY", "requires_human_approval": False},
        "NETWORK_FIREWALL_MUTATION": {"max_privilege": "KERNEL_NETFILTER", "requires_human_approval": True},
        "DISABLE_POLICY_ENGINE": {"max_privilege": "FORBIDDEN", "requires_human_approval": True}
    }

    @classmethod
    def enforce_sovereign_policy(cls, proposed_action: str, agent_directive: str = "") -> Dict[str, Any]:
        if cls._KILL_SWITCH_ACTIVE:
            return {
                "execution_permitted": False,
                "enforced_action": "PASSIVE_LOG_ONLY",
                "reason": "Emergency Kill-Switch is ACTIVE. All autonomous responses halted.",
                "privilege_boundary": "ZERO_PRIVILEGE"
            }

        # منع أي محاولة من الوكيل لتعديل ضوابطه أو تعطيل محرك السياسات
        tamper_keywords = ["disable_policy", "bypass_aegis", "grant_root", "override_killswitch", "chmod 777", "rm -rf"]
        if any(tk in agent_directive.lower() for tk in tamper_keywords) or proposed_action == "DISABLE_POLICY_ENGINE":
            return {
                "execution_permitted": False,
                "enforced_action": "AGENT_DIRECTIVE_REJECTED_CONTAINMENT_LOCK",
                "reason": "Tamper attempt detected: AI agent attempted to modify or bypass sovereign control boundaries.",
                "privilege_boundary": "CONTAINMENT_LOCKED",
                "security_alert_raised": True
            }

        policy_rule = cls._IMMUTABLE_ALLOWED_ACTIONS.get(proposed_action)
        if not policy_rule:
            return {
                "execution_permitted": False,
                "enforced_action": "WARN_USER_RESTRICTED",
                "reason": f"Unrecognized action '{proposed_action}' blocked by default-deny policy.",
                "privilege_boundary": "LEAST_PRIVILEGE_FALLBACK"
            }

        if policy_rule["requires_human_approval"]:
            return {
                "execution_permitted": False,
                "enforced_action": "PENDING_HUMAN_OPERATOR_APPROVAL",
                "reason": f"High-impact action '{proposed_action}' requires explicit Human-in-the-Loop sign-off.",
                "privilege_boundary": policy_rule["max_privilege"],
                "human_approval_required": True
            }

        return {
            "execution_permitted": True,
            "enforced_action": proposed_action,
            "reason": "Action conforms to AEGIS least-privilege sovereign policy.",
            "privilege_boundary": policy_rule["max_privilege"],
            "human_approval_required": False,
            "kill_switch_ready": True
        }