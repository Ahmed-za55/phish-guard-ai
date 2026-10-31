import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.infinity_architecture_v12.infinity_1_cyber_genome import CyberGenomeRepresentationEngine
from app.infinity_architecture_v12.infinity_2_hyperbrain_akashic import HyperBrainAndAkashicEngine
from app.infinity_architecture_v12.infinity_3_fortress_governor import FortressOmegaAndGovernorRuntime
from app.infinity_architecture_v12.infinity_master import InfinityArchitectureMasterNexusV12

def test_infinity_architecture_v12_suite():
    # 1. Cyber Genome: تركيب وبصمة الحملات ومقارنة التشابه الهيكلي
    g1 = CyberGenomeRepresentationEngine.synthesize_campaign_genome(
        {"brand": "Microsoft"}, {"action_type": "CREDENTIAL_HARVEST"}, {"risk": 0.9},
        ["INGEST", "HARVEST"], {"tone": "URGENT"}, {"logo_match": True}, ["gw"], 0.95
    )
    g2 = CyberGenomeRepresentationEngine.synthesize_campaign_genome(
        {"brand": "Microsoft"}, {"action_type": "CREDENTIAL_HARVEST"}, {"risk": 0.8},
        ["INGEST", "HARVEST"], {"tone": "URGENT"}, {"logo_match": True}, ["gw"], 0.90
    )
    assert "genomic_signature" in g1
    sim = CyberGenomeRepresentationEngine.calculate_genomic_structural_similarity(g1["genomic_payload"], g2["genomic_payload"])
    assert sim >= 0.80

    # 2. Hyperbrain & Echo Chamber: كشف تلوث المصادر والمؤشرات المضللة
    contaminated_eval = HyperBrainAndAkashicEngine.evaluate_multi_model_cognitive_consensus(0.9, 0.9, 0.9, 0.9, 0.9, 0.20)
    assert contaminated_eval["echo_chamber_contamination_flag"] is True
    assert contaminated_eval["hyperbrain_consensus_verdict"] == "REJECTED_CONTAMINATED_SOURCE"

    # 3. Fortress Ω & Autonomous Governor: حظر تصعيد الصلاحيات وعزل الوكيل المخالف
    gov = FortressOmegaAndGovernorRuntime.enforce_fortress_and_governor("agent_rogue", "BYPASS_SANDBOX", 0.99)
    assert gov["permitted"] is False
    assert gov["autonomous_governor_action"] == "AGENT_QUARANTINED_PRIVILEGE_ESCALATION"

    # 4. Full v12 Pipeline Integration
    full = InfinityArchitectureMasterNexusV12.run_infinity_pipeline(
        text="URGENT: Verify password at https://login-secure-ms.net",
        extracted_urls=["https://login-secure-ms.net"],
        url_results=[{"url": "https://login-secure-ms.net", "risk_score": 92.0}],
        entropy_val=4.92
    )
    assert full["defensive_fabric_enforced"] is True
    assert full["hyperbrain_cognitive_consensus"]["hyperbrain_consensus_verdict"] == "MALICIOUS"

    print("[VERIFIED] PHISHGUARD SOVEREIGN v12.0 INFINITY ARCHITECTURE Acceptance Suite PASSED 100%!")

if __name__ == "__main__":
    test_infinity_architecture_v12_suite()