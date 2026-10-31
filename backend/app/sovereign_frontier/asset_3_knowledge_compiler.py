import hashlib
import json
from typing import Dict, Any, List, Callable

class SecurityKnowledgeCompiler:
    """
    الأصل الاستراتيجي الثالث: Security Knowledge Compiler.
    يحول المعرفة البحثية المكتوبة بصيغة منظمة (Structured Threat Research Spec)
    إلى:
    1. دالة كشف تنفيذية حقيقية (Compiled Executable Detector).
    2. سياسة استجابة قابلة للتنفيذ.
    3. حالات اختبار تحقق آلية (Positive & Negative Regression Test Cases) للتأكد من سلامة القاعدة قبل نشرها.
    """
    SUPPORTED_OPERATORS = {
        ">=": lambda a, b: float(a) >= float(b),
        "<=": lambda a, b: float(a) <= float(b),
        "==": lambda a, b: str(a).lower() == str(b).lower(),
        "CONTAINS": lambda a, b: str(b).lower() in str(a).lower()
    }

    @classmethod
    def compile_research_advisory(cls, advisory_spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        advisory_spec format:
        {
            "advisory_id": "RES-2026-OAUTH-BEC",
            "title": "OAuth Consent Phishing with Financial Invoice Pivot",
            "conditions": [
                {"field": "oauth_risky_scope", "op": "==", "value": "true"},
                {"field": "domain_age_days", "op": "<=", "value": 14},
                {"field": "lure_text", "op": "CONTAINS", "value": "invoice"}
            ],
            "recommended_action": "REVOKE_TOKEN_AND_QUARANTINE_SESSION",
            "compliance_mapping": ["NIST-IR-4", "ISO27001-A.16"]
        }
        """
        conditions = advisory_spec.get("conditions", [])
        for cond in conditions:
            if cond["op"] not in cls.SUPPORTED_OPERATORS:
                raise ValueError(f"Unsupported operator in knowledge compiler: {cond['op']}")

        # 1. بناء دالة الكشف التنفيذية المترجمة (Compiled Predicate Closure)
        def compiled_detector(telemetry_context: Dict[str, Any]) -> bool:
            for c in conditions:
                field_val = telemetry_context.get(c["field"])
                if field_val is None:
                    return False
                op_fn = cls.SUPPORTED_OPERATORS[c["op"]]
                if not op_fn(field_val, c["value"]):
                    return False
            return True

        # 2. توليد حالات اختبار تلقائية (Synthetic Positive & Benign Negative Test Cases)
        positive_test_case = {}
        negative_test_case = {}
        for c in conditions:
            f, op, val = c["field"], c["op"], c["value"]
            if op == "==":
                positive_test_case[f] = val
                negative_test_case[f] = "BENIGN_DIFFERENT_VALUE"
            elif op == ">=":
                positive_test_case[f] = float(val) + 5.0
                negative_test_case[f] = float(val) - 5.0
            elif op == "<=":
                positive_test_case[f] = max(0.0, float(val) - 2.0)
                negative_test_case[f] = float(val) + 30.0
            elif op == "CONTAINS":
                positive_test_case[f] = f" Urgent corporate {val} attached "
                negative_test_case[f] = "Normal routine weekly sync"

        # 3. تشغيل الاختبارات الذاتية قبل اعتماد القاعدة
        pos_triggered = compiled_detector(positive_test_case)
        neg_triggered = compiled_detector(negative_test_case)
        pre_deployment_verified = (pos_triggered is True) and (neg_triggered is False)

        rule_ast_signature = hashlib.sha256(
            json.dumps(advisory_spec, sort_keys=True).encode("utf-8")
        ).hexdigest()

        return {
            "advisory_id": advisory_spec["advisory_id"],
            "compiled_detector_fn": compiled_detector,
            "enforced_policy_action": advisory_spec["recommended_action"],
            "compliance_evidence_tags": advisory_spec.get("compliance_mapping", []),
            "auto_generated_positive_test_passed": pos_triggered,
            "auto_generated_negative_test_passed": not neg_triggered,
            "pre_deployment_verification_passed": pre_deployment_verified,
            "compiled_rule_sha256": rule_ast_signature
        }