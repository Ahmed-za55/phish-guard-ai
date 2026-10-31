import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.extreme_architecture_v14.extreme_1_reality_reconstruction import CyberRealityReconstructionEngine
from app.extreme_architecture_v14.extreme_2_architecture_auditor import AutonomousArchitectureAuditor
from app.extreme_architecture_v14.extreme_3_adversarial_simulator import AdversarialRealitySimulator
from app.extreme_architecture_v14.extreme_4_constitution_economics import AdaptiveConstitutionAndEconomics
from app.extreme_architecture_v14.extreme_5_continuity_unknown import MissionContinuityAndUnknownDiscovery
from app.extreme_architecture_v14.extreme_master import ExtremeArchitectureMasterNexusV14

def test_extreme_architecture_v14_suite():
    # 1. Reality Reconstruction: إعادة بناء التسلسل وتحديد نقطة البدء
    timeline = CyberRealityReconstructionEngine.reconstruct_attack_timeline([
        {"event_id": "EVT_START", "timestamp": 50, "verified": True},
        {"event_id": "EVT_MID", "timestamp": 70, "verified": True}
    ])
    assert timeline["reconstruction_status"] == "COMPLETED_EVIDENCE_SUPPORTED"
    assert timeline["root_cause_entry_point"] == "EVT_START"

    # 2. Autonomous Architecture Auditor: فحص البنية ورفض الصلاحيات الزائدة
    audit = AutonomousArchitectureAuditor.audit_system_topology([
        {"name": "core_db", "is_single_point_of_failure": True, "has_excessive_privileges": True, "trust_boundary_violation": False}
    ])
    assert audit["architecture_healthy"] is False
    assert "core_db" in audit["single_points_of_failure"]

    # 3. Adversarial Reality Simulator: محاكاة الهجوم المعقد
    sim = AdversarialRealitySimulator.simulate_adaptive_adversary_run("test_sim", True, [])
    assert sim["adversarial_attack_defended"] is True

    # 4. Decision Economics: حساب الخسارة المتوقعة (Expected Loss)
    econ = AdaptiveConstitutionAndEconomics.evaluate_decision_economics(0.92, 50000.0, 100.0)
    assert econ["optimal_economic_action"] == "BLOCK_THREAT"

    # 5. Mission Continuity & Unknown Discovery
    cont = MissionContinuityAndUnknownDiscovery.enforce_mission_continuity(True, True)
    assert cont["fail_closed_enforced"] is True

    unk = MissionContinuityAndUnknownDiscovery.discover_unknown_behavioral_patterns(3.9, 8)
    assert unk["unknown_campaign_pattern_discovered"] is True

    # 6. Full v14 Pipeline Integration
    full = ExtremeArchitectureMasterNexusV14.run_extreme_architecture_pipeline(
        text="Analyze transaction payment at https://secure-bank-portal.org",
        extracted_urls=["https://secure-bank-portal.org"],
        url_results=[{"url": "https://secure-bank-portal.org", "risk_score": 88.0}]
    )
    assert full["extreme_architecture_version"] == "PHISHGUARD_SOVEREIGN_v14.0_EXTREME_EVOLUTION"

    print("[VERIFIED] PHISHGUARD SOVEREIGN v14.0 EXTREME ARCHITECTURE Acceptance Suite PASSED 100%!")

if __name__ == "__main__":
    test_extreme_architecture_v14_suite()