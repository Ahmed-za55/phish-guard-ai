import hashlib
from typing import Dict, Any, List
from app.ascension_omega_v78.ascension_l01_l02_kernel import AscensionSecurityKernelAndTrust
from app.ascension_omega_v78.ascension_l03_l04_cognitive import AscensionDataFabricAndCognitive
from app.ascension_omega_v78.ascension_l05_l06_l07_intel import AscensionDetectionGlobalAndPredictive
from app.ascension_omega_v78.ascension_l08_l09_defense import AscensionAdversarialAndDefenseOrchestrator
from app.ascension_omega_v78.ascension_l10_to_l14_evaluation import AscensionAssuranceMetaAndEvaluation

class AscensionOmegaMasterNexusV78:
    """
    المنسق المركزي لبرنامج ASCENSION Ω (v78):
    يشغل الطبقات الأربع عشرة بالكامل مستنداً إلى Sovereign Meta-Defense و Kernel و Cognitive Engine.
    """
    @staticmethod
    def run_ascension_master_pipeline(
        text: str,
        extracted_urls: List[str],
        url_results: List[Dict[str, Any]],
        ast_triggered: bool,
        entropy_val: float
    ) -> Dict[str, Any]:
        payload_sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
        max_url_risk = max([float(u.get("risk_score", 0.0)) for u in url_results], default=0.0)

        # L03 & L04: Cognitive & Contradiction Resolution
        cognitive = AscensionDataFabricAndCognitive.resolve_contradictions_and_execute_cognitive(
            text, "SAFE" if max_url_risk < 50 else "SUSPICIOUS", max_url_risk, entropy_val
        )

        # L05, L06 & L07: Detection & Unknowns Discovery
        detection = AscensionDetectionGlobalAndPredictive.analyze_unknowns_and_evolution(text, max_url_risk, entropy_val)

        # L08 & L09: Adversarial & Byzantine Defense
        defense = AscensionAdversarialAndDefenseOrchestrator.execute_defense_and_mutation_tests([max_url_risk, 75.0, 999.0], compromised_component=None)

        # L10 to L14: Meta-Defense & Evaluation
        evaluation = AscensionAssuranceMetaAndEvaluation.execute_meta_defense_and_evaluation_pipeline("v78.0", current_fpr=0.009)

        # L01 & L02: Sovereign Security Kernel & Proof-Carrying Decision
        enforced_action = "QUARANTINE_SESSION" if max_url_risk >= 70.0 or ast_triggered else "WARN_USER_RESTRICTED"
        kernel_proof = AscensionSecurityKernelAndTrust.evaluate_independent_kernel(enforced_action, "ascension_omega_agent_01", payload_sha[:24])

        return {
            "ascension_omega_tier": "PHISHGUARD_SOVEREIGN_ASCENSION_OMEGA_v78",
            "sovereign_security_kernel": kernel_proof,
            "cognitive_and_contradiction_engine": cognitive,
            "unknown_unknowns_and_evolution": detection,
            "adversarial_and_byzantine_defense": defense,
            "meta_defense_and_independent_evaluation": evaluation
        }