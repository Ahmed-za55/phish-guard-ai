import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.frontier_v72.trust_verification_plane import TrustAndVerificationPlane
from app.frontier_v72.detection_intelligence import FrontierDetectionIntelligence
from app.frontier_v72.temporal_causal_graph import TemporalAndCausalThreatGraph
from app.frontier_v72.validation_lab import ContinuousValidationAndTwinLab
from app.frontier_v72.controlled_agents import ControlledAgentsAndCollaborativeLearning
from app.frontier_v72.resilient_runtime import ResilientContainmentAndHealingRuntime

def test_all_15_frontier_capabilities():
    # 1. Formal Policy Verification
    fp = TrustAndVerificationPlane.verify_formal_policy_invariants("ISOLATE_COMPONENT", has_authorization=False, active_policies=["DEFAULT_DENY"])
    assert fp["formal_verification_passed"] is False and fp["unsafe_state_path_blocked"] is True

    # 2. Verifiable Runtime & Supply Chain
    sc = TrustAndVerificationPlane.attest_runtime_and_supply_chain()
    assert sc["sbom_verified"] is True and sc["supply_chain_status"] == "VERIFIED_INTACT"

    # 3. Distributed Evidence Verification
    de = TrustAndVerificationPlane.verify_distributed_evidence(["ev1", "ev2"], ["sig_node1", "sig_node2"])
    assert de["distributed_evidence_verified"] is True

    # 4 & 5. Uncertainty-Aware Detection & Conformal Risk Control
    uc = FrontierDetectionIntelligence.evaluate_uncertainty_and_conformal_risk(raw_score=51.0, evidence_count=1)
    assert uc["abstain_and_escalate_to_human"] is True and len(uc["conformal_prediction_set"]) == 2

    # 6. Privacy-Preserving Inference
    pp = FrontierDetectionIntelligence.sanitize_privacy_preserving_input("Contact ahmed@example.com or card 1234567890123456")
    assert pp["pii_redacted"] is True and "[REDACTED_EMAIL]" in pp["sanitized_text"]

    # 7 & 8. Temporal Threat Graph & Causal Threat Analysis
    tc = TemporalAndCausalThreatGraph.analyze_temporal_and_causal_chain(
        [{"url": "http://bad-login.com", "risk_score": 85}], ast_triggered=True, urgency_triggered=True, homograph_triggered=False
    )
    assert tc["causal_threat_analysis"]["verified_causal_attack_progression"] is True

    # 9. Predictive Cyber Digital Twin (Residual Risk)
    dt = ContinuousValidationAndTwinLab.run_predictive_digital_twin(90.0, "BLOCK_AND_QUARANTINE", [{"url": "http://evil.com"}])
    assert dt["residual_risk_after_response"] < 10.0 and dt["safety_test_passed"] is True

    # 10 & 11. Adaptive Adversarial Defense & Continuous Security Validation Lab
    av = ContinuousValidationAndTwinLab.evaluate_adaptive_adversarial_and_ci_gate("normal text", [{"url": "http://evil.com", "risk_score": 80}], model_verdict=False)
    assert av["adversarial_evasion_regression"] is True and av["continuous_validation_release_gate"] == "BLOCKED_REGRESSION_DETECTED"

    # 12. Verified Agent Protocols
    ap = ControlledAgentsAndCollaborativeLearning.enforce_verified_agent_protocol("MUTATE_KERNEL", steps_taken=2)
    assert ap["agent_contract_honored"] is False and ap["protocol_enforcement"] == "TERMINATED_CONTRACT_VIOLATION"

    # 13. Collaborative Threat Learning (Poisoning Resistance)
    cl = ControlledAgentsAndCollaborativeLearning.aggregate_collaborative_threat_intel([80.0, 82.0, 79.0, 999.0])
    assert cl["poisoned_updates_rejected"] == 1 and 78.0 <= cl["collaborative_consensus_score"] <= 83.0

    # 14 & 15. Autonomous Compromise Containment & Self-Healing Distributed Defense
    cc = ResilientContainmentAndHealingRuntime.contain_compromised_component("worker_1", anomaly_detected=True, policy_authorized=True)
    sh = ResilientContainmentAndHealingRuntime.execute_policy_bounded_self_healing("api_svc", service_healthy=False, policy_allows_restart=True)
    assert cc["privileges_revoked"] is True and cc["isolated_tasks_quarantined"] is True
    assert sh["policy_boundary_respected"] is True and sh["rollback_available"] is True

    print("[VERIFIED] All 15 Frontier Architecture & Research Capabilities (6 Planes) PASSED 100%!")

if __name__ == "__main__":
    test_all_15_frontier_capabilities()