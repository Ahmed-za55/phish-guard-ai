import hashlib
import json
from typing import Dict, Any, List, Set

class VerifiableAutonomousDefenseKernel:
    """
    الركيزة الثالثة: الدفاع المستقل القابل للتحقق (Verifiable Autonomous Defense).
    يفصل تماماً بين توصية الـ AI وبين محرك السياسات الحتمي (Deterministic Policy Engine):
    1. يوثق الأدلة ومصادرها ومستوى عدم اليقين.
    2. يحلل البدائل المتاحة ويوثق سبب رفض كل بديل (Rejected Alternatives Ledger).
    3. يتحقق من صلاحيات المكون المنفذ.
    4. يصدر إيصال قرار حتمي قابل لإعادة التشغيل والتحقق التشفيري (Deterministic Replay Verification).
    """
    _COMPONENT_PERMISSIONS: Dict[str, Set[str]] = {
        "enforcer_gateway_01": {"ALLOW_TRAFFIC", "STEP_UP_CHALLENGE", "ISOLATE_SESSION", "BLOCK_DOMAIN"},
        "enforcer_readonly_02": {"ALLOW_TRAFFIC"}
    }

    CANDIDATE_ACTIONS = [
        {"action": "ALLOW_TRAFFIC", "min_risk": 0.0, "max_risk": 0.34, "max_uncertainty": 0.45},
        {"action": "STEP_UP_CHALLENGE", "min_risk": 0.35, "max_risk": 0.74, "max_uncertainty": 1.00},
        {"action": "ISOLATE_SESSION", "min_risk": 0.75, "max_risk": 0.89, "max_uncertainty": 0.40},
        {"action": "BLOCK_DOMAIN", "min_risk": 0.90, "max_risk": 1.00, "max_uncertainty": 0.25}
    ]

    @classmethod
    def execute_verifiable_decision(
        cls,
        executing_component: str,
        evidence_items: List[Dict[str, Any]],
        ai_recommended_risk: float,
        uncertainty_level: float,
        policy_version: str = "SOVEREIGN_POLICY_v15.0"
    ) -> Dict[str, Any]:
        # 1. حساب وزن الأدلة الحتمي المستقل عن الـ AI
        verified_sources = [e["source"] for e in evidence_items if e.get("verified", True)]
        evidence_score = sum(float(e.get("severity", 0.0)) * float(e.get("reliability", 1.0)) for e in evidence_items)
        normalized_evidence_risk = min(1.0, round((evidence_score / max(len(evidence_items), 1)) * 0.6 + (ai_recommended_risk * 0.4), 4))

        # 2. تقييم جميع البدائل وتوثيق أسباب رفض البدائل الأخرى
        selected_action = None
        rejected_alternatives = []

        for candidate in cls.CANDIDATE_ACTIONS:
            act = candidate["action"]
            r_min, r_max = candidate["min_risk"], candidate["max_risk"]
            u_max = candidate["max_uncertainty"]

            if not (r_min <= normalized_evidence_risk <= r_max):
                rejected_alternatives.append({
                    "alternative_action": act,
                    "rejection_reason": f"Normalized risk {normalized_evidence_risk} outside policy band [{r_min}, {r_max}]."
                })
            elif uncertainty_level > u_max:
                rejected_alternatives.append({
                    "alternative_action": act,
                    "rejection_reason": f"Uncertainty {uncertainty_level} exceeds maximum allowed threshold {u_max} for irreversible action."
                })
            elif selected_action is None:
                selected_action = act
            else:
                rejected_alternatives.append({
                    "alternative_action": act,
                    "rejection_reason": f"Superseded by higher-priority matching policy action '{selected_action}'."
                })

        # إذا رُفض الإجراء الصارم بسبب عدم اليقين العالي، نتحول حتمياً إلى STEP_UP_CHALLENGE
        if selected_action is None:
            selected_action = "STEP_UP_CHALLENGE"

        # 3. فحص صلاحيات المكون المنفذ (Component Authorization Check)
        allowed_actions = cls._COMPONENT_PERMISSIONS.get(executing_component, set())
        component_authorized = selected_action in allowed_actions
        final_executed_outcome = selected_action if component_authorized else "HALTED_UNAUTHORIZED_COMPONENT"

        # 4. بناء سجل القرار الحتمي القابل لإعادة الإنتاج
        deterministic_envelope = {
            "policy_governing_decision": policy_version,
            "executing_component": executing_component,
            "component_authorized": component_authorized,
            "evidence_used": evidence_items,
            "evidence_sources": sorted(verified_sources),
            "normalized_evidence_risk": normalized_evidence_risk,
            "uncertainty_level": round(uncertainty_level, 4),
            "selected_action": selected_action,
            "rejected_alternatives": rejected_alternatives,
            "execution_outcome": final_executed_outcome
        }

        canonical_bytes = json.dumps(deterministic_envelope, sort_keys=True).encode("utf-8")
        reproducibility_digest = hashlib.sha256(canonical_bytes).hexdigest()

        return {
            **deterministic_envelope,
            "reproducible_decision_sha256": reproducibility_digest
        }

    @classmethod
    def replay_and_verify_decision(cls, original_decision_record: Dict[str, Any], raw_ai_risk: float) -> Dict[str, Any]:
        """إعادة تشغيل القرار من نفس المدخلات والتأكد من تطابق البصمة التشفيرية والبدائل المرفوضة 100%."""
        replayed = cls.execute_verifiable_decision(
            executing_component=original_decision_record["executing_component"],
            evidence_items=original_decision_record["evidence_used"],
            ai_recommended_risk=raw_ai_risk,
            uncertainty_level=original_decision_record["uncertainty_level"],
            policy_version=original_decision_record["policy_governing_decision"]
        )
        hash_matches = (replayed["reproducible_decision_sha256"] == original_decision_record["reproducible_decision_sha256"])
        return {
            "replay_verified": hash_matches,
            "original_sha256": original_decision_record["reproducible_decision_sha256"],
            "replayed_sha256": replayed["reproducible_decision_sha256"]
        }