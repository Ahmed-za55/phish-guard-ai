from typing import Dict, Any, List
from app.apocalypse_frontier_v9.apocalypse_1_project_aegis import ProjectAegisSecurityKernel
from app.apocalypse_frontier_v9.apocalypse_2_project_origin import ProjectOriginEvidenceProvenance

class ApocalypsePhase1MasterNexus:
    """
    المنسق المركزي للمرحلة الأولى من APOCALYPSE FRONTIER (AEGIS + ORIGIN):
    يؤمن بيئة التشغيل ويوثق أصل الأدلة لكل عملية كشف تجري في النظام.
    """
    @staticmethod
    def run_apocalypse_phase_1_pipeline(
        text: str,
        extracted_urls: List[str],
        url_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        max_url_risk = max([float(u.get("risk_score", 0.0)) for u in url_results], default=0.0)

        # 1. Project Aegis: Runtime Capability Check
        kernel_auth = ProjectAegisSecurityKernel.enforce_runtime_capability("threat_detector", "ANALYZE_TEXT")

        # 2. Project Origin: Evidence Provenance Seal
        verdict = "MALICIOUS" if max_url_risk >= 70.0 else "SAFE"
        provenance_seal = ProjectOriginEvidenceProvenance.record_evidence_provenance(
            evidence_source="orchestrator_ingress",
            raw_payload_snippet=text[:80],
            derived_verdict=verdict
        )

        return {
            "apocalypse_frontier_phase": "PHISHGUARD_APOCALYPSE_PHASE_1_AEGIS_ORIGIN",
            "project_aegis_kernel": kernel_auth,
            "project_origin_provenance": provenance_seal
        }