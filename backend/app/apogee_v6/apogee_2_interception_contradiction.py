from urllib.parse import urlparse
from typing import Dict, Any, List

class PreExecutionAndContradictionEngine:
    """
    1. Pre-Execution Security Interception: طبقة اعتراض حتمية (Deterministic) تعمل قبل الفتح أو المعالجة ولا تعتمد على الـ AI وحده.
    2. Intelligence Contradiction Resolution: حل التعارض بين المصادر (مثل قائمة بيضاء قديمة مقابل سلوك صفحة خبيث).
    """
    BLOCKED_SCHEMES = {"javascript", "data", "vbscript", "file"}
    DANGEROUS_EXTENSIONS = (".exe", ".scr", ".vbs", ".bat", ".ps1", ".hta", ".iso")

    @classmethod
    def intercept_pre_execution(cls, urls: List[str], filenames: List[str], requested_permission: str) -> Dict[str, Any]:
        intercepted_reasons = []

        for u in urls:
            parsed = urlparse(u)
            if (parsed.scheme or "").lower() in cls.BLOCKED_SCHEMES:
                intercepted_reasons.append(f"DETERMINISTIC_BLOCK_SCHEME:{parsed.scheme}")
            if any(u.lower().endswith(ext) for ext in cls.DANGEROUS_EXTENSIONS):
                intercepted_reasons.append("DETERMINISTIC_BLOCK_EXECUTABLE_URL")

        for f in filenames:
            if any(f.lower().endswith(ext) for ext in cls.DANGEROUS_EXTENSIONS):
                intercepted_reasons.append(f"DETERMINISTIC_BLOCK_FILE:{f}")

        if requested_permission in {"SYSTEM_SHELL", "RAW_SOCKET", "UNRESTRICTED_FS"}:
            intercepted_reasons.append(f"DETERMINISTIC_BLOCK_PERMISSION:{requested_permission}")

        blocked = len(intercepted_reasons) > 0
        return {
            "pre_execution_blocked": blocked,
            "deterministic_policy_enforced": True,
            "interception_reasons": intercepted_reasons,
            "gate_action": "PRE_EXECUTION_DROP" if blocked else "ALLOW_TO_SANDBOX"
        }

    @staticmethod
    def resolve_intelligence_contradictions(evidence_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        كل عنصر دليل يحتوي على: source, verdict (SAFE / MALICIOUS), reliability (0-1), age_hours
        """
        if not evidence_items:
            return {"final_resolution": "UNKNOWN_NEEDS_REVIEW", "contradiction_found": False}

        verdicts = set()
        fresh_malicious_weight = 0.0
        fresh_safe_weight = 0.0
        stale_sources_ignored = 0

        for item in evidence_items:
            age = item.get("age_hours", 0)
            rel = item.get("reliability", 0.5)
            v = item.get("verdict", "UNKNOWN")
            verdicts.add(v)

            # إضعاف الأدلة القديمة (أكثر من 72 ساعة)
            freshness_factor = 0.2 if age > 72 else 1.0
            if age > 72:
                stale_sources_ignored += 1

            weight = rel * freshness_factor
            if v == "MALICIOUS":
                fresh_malicious_weight += weight
            elif v == "SAFE":
                fresh_safe_weight += weight

        contradiction_found = ("SAFE" in verdicts and "MALICIOUS" in verdicts)

        # منع اتخاذ قرار آمن بناءً على مصدر واحد عند وجود تعارض سلوكي حديث
        if fresh_malicious_weight >= 0.6:
            resolution = "MALICIOUS_CONFIRMED_BY_BEHAVIOR"
        elif contradiction_found and abs(fresh_malicious_weight - fresh_safe_weight) < 0.3:
            resolution = "NEEDS_HUMAN_REVIEW_CONTRADICTED"
        elif fresh_safe_weight >= 0.7 and not contradiction_found:
            resolution = "SAFE_VERIFIED"
        else:
            resolution = "UNKNOWN_INSUFFICIENT_EVIDENCE"

        return {
            "contradiction_found": contradiction_found,
            "stale_sources_discounted": stale_sources_ignored,
            "malicious_evidence_weight": round(fresh_malicious_weight, 2),
            "safe_evidence_weight": round(fresh_safe_weight, 2),
            "final_resolution": resolution
        }