from typing import Dict, Any, List
from app.beyond_frontier_v73.sovereign_trust_plane import SovereignTrustPlane
from app.beyond_frontier_v73.secure_evidence_ingestion import SecureEvidenceIngestionPlane
from app.beyond_frontier_v73.detection_fabric import BeyondDetectionFabric
from app.beyond_frontier_v73.threat_intelligence_plane import ThreatIntelligencePlane
from app.beyond_frontier_v73.risk_adjudication_plane import RiskAdjudicationPlane
from app.beyond_frontier_v73.adversarial_evolution_lab import AdversarialEvolutionAndSelfImprovementLab
from app.beyond_frontier_v73.policy_gated_response import PolicyGatedResponseAndExchangePlane
from app.beyond_frontier_v73.independent_assurance import IndependentAssuranceAndBenchmarkPlane

class BeyondFrontierNexusV73:
    """
    يدير دورة حياة الفحص والتحقق عبر الطبقات الثماني الكاملة لحزمة Beyond Frontier v73.
    """
    @staticmethod
    def run_beyond_frontier_architecture(
        raw_text: str,
        extracted_urls: List[str],
        url_results: List[Dict[str, Any]],
        ast_triggered: bool,
        homograph_triggered: bool,
        urgency_triggered: bool,
        entropy_val: float,
        tda_score: float
    ) -> Dict[str, Any]:
        # Plane 2: Secure Evidence Ingestion & Canary Check
        ingestion = SecureEvidenceIngestionPlane.inspect_and_ingest_evidence(raw_text, extracted_urls)
        canary = SecureEvidenceIngestionPlane.verify_canary_pipeline_integrity()

        # Plane 3: Detection Fabric (Multi-Agent Adjudication & Unknown Threat Discovery)
        max_url_risk = max([float(u.get("risk_score", 0.0)) for u in url_results], default=0.0)
        ast_score = 85.0 if ast_triggered else 5.0
        homo_score = 95.0 if homograph_triggered else 0.0
        vis_score = 75.0 if homograph_triggered else (40.0 if max_url_risk >= 50 else 5.0)

        adjudication = BeyondDetectionFabric.adjudicate_independent_analyzers(
            lexical_score=max_url_risk,
            ast_score=ast_score,
            homograph_score=homo_score,
            vision_score=vis_score
        )
        known_rule_hit = bool(max_url_risk >= 45.0 or ast_triggered or homograph_triggered)
        unknown_discovery = BeyondDetectionFabric.discover_unknown_threats(
            entropy_val=entropy_val, tda_score=tda_score, known_rule_matched=known_rule_hit
        )

        # Plane 4: Threat Intelligence (Attack-Path Reconstruction, Causal Discovery, Early Forecasting)
        threat_intel = ThreatIntelligencePlane.reconstruct_attack_path_and_causality(
            url_results, urgency_triggered, ast_triggered, homograph_triggered
        )

        # Plane 5: Risk Adjudication (Counterfactual Simulator & Distribution-Free Risk Control)
        risk_adjudication = RiskAdjudicationPlane.simulate_counterfactual_decisions(
            adjudicated_risk_score=adjudication["adjudicated_risk_score"],
            disagreement_std=adjudication["inter_analyzer_disagreement_std"]
        )

        # Plane 1: Sovereign Trust Plane (Zero-Trust Fabric, Formal Safety Kernel, Verified Agent Chain)
        agent_chain = [
            {"agent": "lexical_analyzer", "op": "READ_URL"},
            {"agent": "vision_analyzer", "op": "READ_IMAGE"},
            {"agent": "orchestrator_agent", "op": "PROPOSE_ACTION"}
        ]
        orchestration_proof = SovereignTrustPlane.verify_agent_orchestration_chain(agent_chain)
        quorum_met = sum(1 for s in [max_url_risk, ast_score, homo_score] if s >= 45.0) >= 2 or max_url_risk >= 75.0
        safety_kernel = SovereignTrustPlane.evaluate_formal_safety_kernel(
            proposed_action=risk_adjudication["counterfactual_optimal_action"],
            independent_quorum_met=quorum_met,
            human_approved=False
        )

        # Plane 6: Adversarial Lab & Safe Self-Improvement
        adversarial_eval = AdversarialEvolutionAndSelfImprovementLab.run_adversarial_evolution_tests(
            raw_text, adjudication["adjudicated_risk_score"]
        )
        self_improvement = AdversarialEvolutionAndSelfImprovementLab.stage_for_safe_self_improvement(
            raw_text, adjudication["adjudicated_risk_score"], adjudication["inter_analyzer_disagreement_std"]
        )

        # Plane 7: Policy-Gated Response & Privacy-Preserving Threat Exchange
        threat_exchange = PolicyGatedResponseAndExchangePlane.prepare_privacy_preserving_threat_exchange(
            url_results, is_confirmed_threat=(safety_kernel["enforced_action"] == "BLOCK_AND_QUARANTINE")
        )

        # Plane 8: Independent Assurance & Benchmark Program
        assurance_benchmark = IndependentAssuranceAndBenchmarkPlane.evaluate_against_strong_baseline(
            raw_text, url_results, safety_kernel["enforced_action"], adjudication["adjudicated_risk_score"]
        )

        return {
            "plane_1_sovereign_trust": {
                "verified_agent_orchestration": orchestration_proof,
                "formal_safety_kernel": safety_kernel
            },
            "plane_2_secure_evidence_ingestion": {
                "evidence_provenance_and_ssrf_guard": ingestion,
                "resilient_canary_system": canary
            },
            "plane_3_detection_fabric": {
                "multi_agent_independent_adjudication": adjudication,
                "unknown_threat_discovery": unknown_discovery
            },
            "plane_4_threat_intelligence": threat_intel,
            "plane_5_risk_adjudication": risk_adjudication,
            "plane_6_adversarial_lab": {
                "adversarial_evolution_tests": adversarial_eval,
                "safe_self_improvement_pipeline": self_improvement
            },
            "plane_7_policy_gated_response": {
                "enforced_safe_action": safety_kernel["enforced_action"],
                "privacy_preserving_threat_exchange": threat_exchange
            },
            "plane_8_independent_assurance": assurance_benchmark
        }