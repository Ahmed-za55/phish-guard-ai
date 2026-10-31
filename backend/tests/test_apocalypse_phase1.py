import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.apocalypse_frontier_v9.apocalypse_1_project_aegis import ProjectAegisSecurityKernel
from app.apocalypse_frontier_v9.apocalypse_2_project_origin import ProjectOriginEvidenceProvenance

def test_apocalypse_phase1_suite():
    # 1. Project Aegis: منع العمليات غير المصرح بها وإيقاف الطوارئ
    auth_ok = ProjectAegisSecurityKernel.enforce_runtime_capability("threat_detector", "ANALYZE_TEXT")
    assert auth_ok["execution_permitted"] is True

    auth_fail = ProjectAegisSecurityKernel.enforce_runtime_capability("threat_detector", "EMERGENCY_SHUTDOWN")
    assert auth_fail["execution_permitted"] is False
    assert auth_fail["unauthorized_escalation_blocked"] is True

    # 2. Project Origin: سجل الأدلة المرتبط تشفيرياً (Hash-Chain)
    prov1 = ProjectOriginEvidenceProvenance.record_evidence_provenance("api_gateway", "test payload alpha", "SAFE")
    prov2 = ProjectOriginEvidenceProvenance.record_evidence_provenance("dom_analyzer", "test payload beta", "MALICIOUS")
    
    assert prov1["sequence_id"] == 0
    assert prov2["sequence_id"] == 1
    assert prov2["previous_provenance_hash"] == prov1["provenance_record_hash"]
    assert prov2["tamper_evident_verified"] is True

    print("[VERIFIED] PHISHGUARD SOVEREIGN v9.0 APOCALYPSE PHASE 1 (AEGIS + ORIGIN) Acceptance Suite PASSED 100%!")

if __name__ == "__main__":
    test_apocalypse_phase1_suite()