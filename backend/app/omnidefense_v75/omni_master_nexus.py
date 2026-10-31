from typing import Dict, Any, List
from app.omnidefense_v75.omni_plane_1_trust_safety import OmniTrustAndSafetyPlane
from app.omnidefense_v75.omni_plane_2_evidence_evidence_ingestion import OmniEvidenceIngestionPlane
from app.omnidefense_v75.omni_plane_3_identity_surface import OmniIdentityAndSurfacePlane
from app.omnidefense_v75.omni_plane_4_detection_reasoning import OmniDetectionAndReasoningPlane
from app.omnidefense_v75.omni_plane_5_intelligence_forecasting import OmniIntelligenceAndForecastingPlane
from app.omnidefense_v75.omni_plane_6_adjudication_risk import OmniAdjudicationAndRiskPlane
from app.omnidefense_v75.omni_plane_7_adversarial_improvement import OmniAdversarialAndImprovementPlane
from app.omnidefense_v75.omni_plane_8_resilience_assurance import OmniResilienceAndAssurancePlane

class OmniDefenseMasterNexusV75:
    """
    المنسق المركزي لبرنامج OMNIDEFENSE (v75):
    ينفذ الطبقات الثماني الكاملة ويطبق القاعدة: لا ذكاء دون أدلة، لا تنفيذ دون صلاحية، لا تحديث دون تحقق.
    """
    @staticmethod
    def run_omnidefense_master_pipeline(
        text: str,
        extracted_urls: List[str],
        url_results: List[Dict[str, Any]],
        ast_triggered: bool,
        homograph_triggered: bool,
        entropy_val: float
    ) -> Dict[str, Any]:
        # Plane 2: Ingestion & SSRF & Evidence Continuity
        ingest_res = OmniEvidenceIngestionPlane.ingest_and_verify_evidence(text, extracted_urls)

        # Plane 3: Identity & Attack Surface
        surface_res = OmniIdentityAndSurfacePlane.analyze_identity_and_attack_surface(text)

        # Plane 4: Detection & Multi-Modal Reasoning
        max_url_risk = max([float(u.get("risk_score", 0.0)) for u in url_results], default=0.0)
        multimodal_res = OmniDetectionAndReasoningPlane.execute_multi_modal_reasoning(
            text, max_url_risk, ast_triggered, homograph_triggered, vision_risk=surface_res["identity_centric_risk_score"]
        )

        # Plane 5: Intelligence & Forecasting
        forecasting_res = OmniIntelligenceAndForecastingPlane.forecast_and_reason_open_world(
            url_results, multimodal_res["adjudicated_multimodal_risk"], entropy_val
        )

        # Plane 6: Adjudication & Counterfactual Risk Simulation
        adjudication_res = OmniAdjudicationAndRiskPlane.evaluate_causal_and_counterfactual_risk(
            multimodal_res["adjudicated_multimodal_risk"]
        )

        # Plane 1: Trust & Safety Kernel
        kernel_res = OmniTrustAndSafetyPlane.evaluate_runtime_safety_kernel(
            proposed_action=adjudication_res["counterfactual_optimal_action"],
            agent_compromised=False,
            human_signoff=False
        )

        # Plane 7: Adversarial Lab & Safe Improvement
        adversarial_res = OmniAdversarialAndImprovementPlane.run_adversarial_testing_and_staging(
            text, multimodal_res["adjudicated_multimodal_risk"]
        )

        # Plane 8: Resilience & Independent Assurance
        assurance_res = OmniResilienceAndAssurancePlane.execute_verified_recovery_and_assurance(
            service_compromised=False,
            optimal_action=kernel_res["enforced_action"]
        )

        return {
            "omnidefense_program_tier": "PHISHGUARD_SOVEREIGN_OMNIDEFENSE_v75",
            "plane_1_trust_and_safety_kernel": kernel_res,
            "plane_2_evidence_ingestion_and_continuity": ingest_res,
            "plane_3_identity_and_surface": surface_res,
            "plane_4_detection_and_multimodal_reasoning": multimodal_res,
            "plane_5_intelligence_and_forecasting": forecasting_res,
            "plane_6_adjudication_and_counterfactual_risk": adjudication_res,
            "plane_7_adversarial_lab_and_improvement": adversarial_res,
            "plane_8_resilience_and_assurance": assurance_res
        }