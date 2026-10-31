import hashlib
from typing import Dict, Any, List
from app.prometheus_omega_v77.prometheus_l0_l1_kernel import PrometheusKernelAndTrust
from app.prometheus_omega_v77.prometheus_l2_l3_cognitive import PrometheusDataFabricAndCognitive
from app.prometheus_omega_v77.prometheus_l4_l5_detection import PrometheusDetectionAndGlobalIntel
from app.prometheus_omega_v77.prometheus_l6_research_engine import SovereignResearchEngine
from app.prometheus_omega_v77.prometheus_l7_l8_l9_defense import PrometheusDefenseAssuranceAndEvaluation

class PrometheusOmegaMasterNexusV77:
    """
    المنسق المركزي لبرنامج PROMETHEUS Ω (v77):
    يشغل الطبقات العشر بالكامل مستنداً إلى الثالوث: Cognitive Engine + Security Kernel + Research Engine.
    """
    @staticmethod
    def run_prometheus_master_pipeline(
        text: str,
        extracted_urls: List[str],
        url_results: List[Dict[str, Any]],
        ast_triggered: bool,
        entropy_val: float
    ) -> Dict[str, Any]:
        payload_sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
        max_url_risk = max([float(u.get("risk_score", 0.0)) for u in url_results], default=0.0)

        # L2 & L3: Data Fabric & Cognitive Reasoning
        cognitive_res = PrometheusDataFabricAndCognitive.process_data_and_execute_cognitive(text, extracted_urls, entropy_val)

        # L4 & L5: Detection Fabric & Global Intel
        detection_res = PrometheusDetectionAndGlobalIntel.analyze_behavioral_dna_and_hypotheses(text, max_url_risk)

        # L6: Sovereign Research Engine Cycle
        research_res = SovereignResearchEngine.execute_research_experiment_cycle(
            anomaly_detected=cognitive_res["cognitive_open_world"]["open_world_anomaly_detected"],
            candidate_hypothesis=detection_res["autonomous_threat_hypothesis"]["hypothesis_description"]
        )

        # L7, L8 & L9: Defense, Assurance & Evaluation
        agent_scores = [max_url_risk, 80.0 if ast_triggered else 10.0, 50.0]
        enforced_action = "QUARANTINE_SESSION" if max_url_risk >= 70.0 or ast_triggered else "WARN_USER_RESTRICTED"

        # L0 & L1: Kernel & Proof-Carrying Decision
        kernel_proof = PrometheusKernelAndTrust.evaluate_kernel_and_issue_proof(
            proposed_action=enforced_action,
            agent_id="prometheus_omega_agent_01",
            evidence_digest=payload_sha[:24],
            model_version="Prometheus-Omega-v77.0"
        )

        defense_eval = PrometheusDefenseAssuranceAndEvaluation.execute_defense_assurance_pipeline(
            agent_scores=agent_scores,
            enforced_action=kernel_proof["enforced_action"]
        )

        return {
            "prometheus_omega_tier": "PHISHGUARD_SOVEREIGN_PROMETHEUS_OMEGA_v77",
            "l0_l1_sovereign_security_kernel": kernel_proof,
            "l2_l3_cognitive_intelligence": cognitive_res,
            "l4_l5_detection_and_global_intel": detection_res,
            "l6_sovereign_research_engine": research_res,
            "l7_l8_l9_defense_assurance": defense_eval
        }