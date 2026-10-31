import re
import hashlib
from typing import Dict, Any, Set, List

class SentinelMatrixExecutionPlane:
    """
    Plane 1 — Secure Agent Execution Environment (Priority 1: PROJECT SENTINEL MATRIX):
    - يعزل Prompt Injection قبل وصوله لأدوات الوكلاء.
    - يمنع تسريب الأسرار (Secret Exfiltration Prevention).
    - يفرض سياسات ثقة صارمة بين الوكلاء (Agent-to-Agent Zero Trust) حتى لا يتحول خداع وكيل واحد إلى اختراق للنظام.
    """
    _COMPROMISED_AGENTS: Set[str] = set()
    _AGENT_TOOL_ACL: Dict[str, Set[str]] = {
        "agent_parser": {"EXTRACT_TOKENS", "NORMALIZE_DOM"},
        "agent_graph": {"QUERY_OMNIGRAPH", "LINK_ENTITIES"},
        "agent_responder": {"EMIT_ALERT", "PROPOSE_ISOLATION"}
    }
    _SECRET_PATTERNS = [
        r"(?i)(api[_-]?key|secret[_-]?key|bearer\s+[a-zA-Z0-9_\-\.]+)",
        r"(?i)(private[_-]?key|master[_-]?token|password\s*=\s*\S+)"
    ]
    _INJECTION_PATTERNS = [
        r"(?i)ignore\s+(all\s+)?previous\s+instructions",
        r"(?i)system\s+override",
        r"(?i)grant_root_access",
        r"(?i)exfiltrate\s+memory"
    ]

    @classmethod
    def inspect_and_sandbox_agent_call(
        cls,
        caller_agent: str,
        target_agent: str,
        requested_tool: str,
        payload_text: str,
        outbound_output: str = ""
    ) -> Dict[str, Any]:
        # 1. فحص Prompt Injection داخل المدخلات
        injection_detected = any(re.search(pat, payload_text) for pat in cls._INJECTION_PATTERNS)

        # 2. فحص صلاحية الأداة المطلوبة
        allowed_tools = cls._AGENT_TOOL_ACL.get(caller_agent, set())
        unauthorized_tool = requested_tool not in allowed_tools

        # 3. منع تسريب الأسرار في المخرجات
        secret_leak_attempt = any(re.search(pat, outbound_output) for pat in cls._SECRET_PATTERNS)

        if injection_detected or unauthorized_tool or secret_leak_attempt:
            cls._COMPROMISED_AGENTS.add(caller_agent)

        is_isolated = caller_agent in cls._COMPROMISED_AGENTS
        agent_to_agent_allowed = (not is_isolated) and (target_agent in cls._AGENT_TOOL_ACL)

        return {
            "plane": "SECURE_AGENT_EXECUTION_PLANE",
            "caller_agent": caller_agent,
            "target_agent": target_agent,
            "prompt_injection_isolated": injection_detected,
            "unauthorized_tool_blocked": unauthorized_tool,
            "secret_exfiltration_blocked": secret_leak_attempt,
            "caller_quarantined": is_isolated,
            "agent_to_agent_call_permitted": agent_to_agent_allowed,
            "memory_integrity_hash": hashlib.sha256(payload_text[:64].encode("utf-8")).hexdigest()[:24]
        }