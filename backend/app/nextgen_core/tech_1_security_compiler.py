import re
import json
import hashlib
from typing import Dict, Any, List, Callable

class AutonomousSecurityCompiler:
    """
    التقنية الأولى: Autonomous Security Compiler.
    ينفذ سلسلة الترجمة الكاملة (8 مراحل):
    Threat Research -> Knowledge Extraction -> Threat Model -> Detection Spec
    -> Policy Generation -> Automated Test Generation -> Security Validation -> Controlled Deployment.
    """
    IndicatorPatterns = {
        "brand_spoof": r"(?i)spoof(?:ing|ed)?\s+([a-zA-Z0-9_\-]+)",
        "max_domain_age": r"(?i)domain\s+age\s*(?:<|under|less\s+than)\s*(\d+)\s*days",
        "risky_scope": r"(?i)oauth\s+scope\s+([a-zA-Z0-9_\.\-]+)",
        "financial_keyword": r"(?i)financial\s+lure\s+containing\s+'([^']+)'",
        "Psychology_lever": r"(?i)psychological\s+lever:\s*(authority|urgency|fear)"
    }

    @classmethod
    def compile_threat_research(cls, raw_research_report: str, report_id: str = "TR-2026-NEXTGEN") -> Dict[str, Any]:
        # المرحلة 1 و 2: Threat Research -> Knowledge Extraction
        extracted: Dict[str, Any] = {}
        for key, pat in cls.IndicatorPatterns.items():
            m = re.search(pat, raw_research_report)
            if m:
                extracted[key] = m.group(1).strip()

        # المرحلة 3: Threat Model Construction
        severity = 0.35
        if "risky_scope" in extracted:
            severity += 0.30
        if "financial_keyword" in extracted:
            severity += 0.25
        if "max_domain_age" in extracted:
            severity += 0.15
        severity = min(0.99, round(severity, 3))

        threat_model = {
            "report_id": report_id,
            "extracted_indicators": extracted,
            "modeled_severity": severity,
            "attack_surface": "CROSS_DOMAIN_IDENTITY_AND_FINANCE" if "risky_scope" in extracted else "EMAIL_INGRESS"
        }

        # المرحلة 4: Detection Specification (AST Predicates)
        predicates_spec = []
        if "max_domain_age" in extracted:
            predicates_spec.append({"field": "domain_age_days", "op": "<=", "val": int(extracted["max_domain_age"])})
        if "risky_scope" in extracted:
            predicates_spec.append({"field": "oauth_scope", "op": "==", "val": extracted["risky_scope"].lower()})
        if "financial_keyword" in extracted:
            predicates_spec.append({"field": "text", "op": "CONTAINS", "val": extracted["financial_keyword"].lower()})
        if "Psychology_lever" in extracted:
            predicates_spec.append({"field": "deception_lever", "op": "==", "val": extracted["Psychology_lever"].lower()})

        # بناء دالة الكشف المترجمة (Compiled Multi-Condition Detector)
        def compiled_detector(event: Dict[str, Any]) -> bool:
            if not predicates_spec:
                return False
            matched = 0
            for p in predicates_spec:
                val = event.get(p["field"])
                if val is None:
                    continue
                if p["op"] == "<=" and float(val) <= float(p["val"]):
                    matched += 1
                elif p["op"] == "==" and str(val).lower() == str(p["val"]).lower():
                    matched += 1
                elif p["op"] == "CONTAINS" and str(p["val"]).lower() in str(val).lower():
                    matched += 1
            # يتطلب تحقق الشرط الهيكلي (العمر أو الـ Scope) مع الشرط الدلالي لمنع الإنذارات الكاذبة
            return matched >= max(1, len(predicates_spec) - 1) and float(event.get("domain_age_days", 999)) <= float(extracted.get("max_domain_age", 30))

        # المرحلة 5: Policy Generation
        policy_action = "REVOKE_OAUTH_AND_HOLD_WIRE" if severity >= 0.80 else "STEP_UP_MFA_CHALLENGE"

        # المرحلة 6: Automated Test Generation (Adversarial Positive, Paraphrased Positive, Hard Benign Negative)
        max_age = int(extracted.get("max_domain_age", 14))
        scope_val = extracted.get("risky_scope", "mail.readwrite").lower()
        fin_word = extracted.get("financial_keyword", "iban").lower()
        lever_val = extracted.get("Psychology_lever", "urgency").lower()

        auto_test_suite = [
            {
                "test_name": "T1_Exact_Threat_Match",
                "expected": True,
                "event": {"domain_age_days": max(1, max_age - 5), "oauth_scope": scope_val, "text": f"Urgent transfer to new {fin_word}", "deception_lever": lever_val}
            },
            {
                "test_name": "T2_Evasive_Paraphrased_Lure_No_Keyword",
                "expected": True,
                "event": {"domain_age_days": max(1, max_age - 3), "oauth_scope": scope_val, "text": "Please authorize account settlement", "deception_lever": lever_val}
            },
            {
                "test_name": "T3_Hard_Benign_Legitimate_Invoice_Old_Domain",
                "expected": False,
                "event": {"domain_age_days": 1200, "oauth_scope": "none", "text": f"Official {fin_word} statement attached", "deception_lever": lever_val}
            }
        ]

        # المرحلة 7: Security Validation
        validation_results = []
        all_passed = True
        for tc in auto_test_suite:
            actual = compiled_detector(tc["event"])
            passed = (actual == tc["expected"])
            if not passed:
                all_passed = False
            validation_results.append({"test": tc["test_name"], "expected": tc["expected"], "actual": actual, "passed": passed})

        # المرحلة 8: Controlled Deployment Artifact
        artifact_hash = hashlib.sha256(json.dumps({"model": threat_model, "spec": predicates_spec, "policy": policy_action}, sort_keys=True).encode()).hexdigest()

        return {
            "stage_1_2_extracted_knowledge": extracted,
            "stage_3_threat_model": threat_model,
            "stage_4_detection_spec": predicates_spec,
            "stage_5_generated_policy": policy_action,
            "stage_6_7_validation_results": validation_results,
            "stage_8_deployment_state": "STAGED_VERIFIED_READY" if all_passed else "QUARANTINED_FAILED_VALIDATION",
            "artifact_sha256": artifact_hash,
            "executable_detector": compiled_detector
        }