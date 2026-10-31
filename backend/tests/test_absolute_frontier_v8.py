import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.absolute_frontier_v8.frontier_genesis import ProjectGenesisDiscovery
from app.absolute_frontier_v8.frontier_prometheus import ProjectPrometheusResearchLab
from app.absolute_frontier_v8.frontier_aegis_core import ProjectAegisCoreRuntime
from app.absolute_frontier_v8.frontier_omniscience_singularity import OmniscienceAndSingularityEngine

def test_absolute_frontier_v8_suite():
    # 1. Project Genesis: اكتشاف التهديدات المجهولة والإنتروبيا العالية
    gen = ProjectGenesisDiscovery.discover_unknown_threats([1.2, 1.4, 3.8, 4.1], text_entropy=5.1)
    assert gen["genesis_unknown_threat_discovered"] is True

    # 2. Project Prometheus: ترقية النموذج بوابياً وتجاوز الانحدار
    prom = ProjectPrometheusResearchLab.run_research_experiment("hyp_01", 0.98, 0.995, True)
    assert prom["research_action"] == "PROMOTE_CHALLENGER_TO_PRODUCTION"

    # 3. Project Aegis Core: حظر العمليات غير المصرح بها وعزل الوكيل
    aegis = ProjectAegisCoreRuntime.enforce_runtime_capability("genesis_agent", "MUTATE_CORE_KERNEL")
    assert aegis["execution_permitted"] is False
    assert aegis["capability_violation_quarantined"] is True

    # 4. Omniscience & Singularity: التناقض متعدد الوسائط
    omni = OmniscienceAndSingularityEngine.evaluate_cross_modal_and_neuro_symbolic(
        text="Please verify Microsoft password immediately",
        urls=["https://evil-harvest-domain.com"],
        claimed_brand="Microsoft",
        dom_password_field=True,
        visual_logo_match=True
    )
    assert omni["neuro_symbolic_constraint_triggered"] is True
    assert omni["final_decision_verdict"] == "MALICIOUS_MULTIMODAL_SPOOF"

    print("[VERIFIED] PHISHGUARD SOVEREIGN v8.0 ABSOLUTE FRONTIER Acceptance Suite PASSED 100%!")

if __name__ == "__main__":
    test_absolute_frontier_v8_suite()