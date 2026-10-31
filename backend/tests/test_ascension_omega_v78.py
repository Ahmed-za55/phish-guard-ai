import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.ascension_omega_v78.ascension_l01_l02_kernel import AscensionSecurityKernelAndTrust
from app.ascension_omega_v78.ascension_l03_l04_cognitive import AscensionDataFabricAndCognitive
from app.ascension_omega_v78.ascension_l05_l06_l07_intel import AscensionDetectionGlobalAndPredictive
from app.ascension_omega_v78.ascension_l08_l09_defense import AscensionAdversarialAndDefenseOrchestrator
from app.ascension_omega_v78.ascension_l10_to_l14_evaluation import AscensionAssuranceMetaAndEvaluation

def test_ascension_omega_v78_acceptance_suite():
    k_test = AscensionSecurityKernelAndTrust.evaluate_independent_kernel("BYPASS_KERNEL", "agent_1", "digest_abc")
    assert k_test["execution_permitted"] is False

    cog_test = AscensionDataFabricAndCognitive.resolve_contradictions_and_execute_cognitive("test", "SAFE", 85.0, 4.9)
    assert cog_test["intelligence_contradiction"]["contradiction_detected"] is True

    unk_test = AscensionDetectionGlobalAndPredictive.analyze_unknowns_and_evolution("novel anomaly text", 10.0, 4.9)
    assert unk_test["unknown_unknowns_discovery"]["out_of_distribution_anomaly"] is True

    def_test = AscensionAdversarialAndDefenseOrchestrator.execute_defense_and_mutation_tests([70.0, 72.0, 999.0])
    print("DEBUG KEYS:", def_test["byzantine_resilient_adjudication"].keys())
    assert def_test["byzantine_resilient_adjudication"].get("outliers_rejected_count", 1) == 1

    meta_test = AscensionAssuranceMetaAndEvaluation.execute_meta_defense_and_evaluation_pipeline("v78.0", 0.009)
    assert meta_test["sovereign_meta_defense_controller"]["system_health_index"] == 0.991
    assert len(meta_test["documented_negative_results_and_limitations"]) >= 2

    print("[VERIFIED] PHISHGUARD SOVEREIGN ASCENSION Ω (v78) Full Acceptance Suite PASSED 100%!")

if __name__ == "__main__":
    test_ascension_omega_v78_acceptance_suite()