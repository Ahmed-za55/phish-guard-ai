import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.apocalypse_v2_0.enterprise_fabric import EnterpriseIntegrationFabric
from app.apocalypse_v2_0.incident_response_forensics import IncidentForensicsAndResponse
from app.apocalypse_v2_0.identity_tenant_security import EnterpriseIdentityAndTenantArchitecture
from app.apocalypse_v2_0.validation_economics import SecurityEffectivenessAndEconomics

def test_apocalypse_v2_0_suite():
    # 1. Multi-Tenant Isolation
    tenant = EnterpriseIdentityAndTenantArchitecture.enforce_tenant_isolation("client_abc", "confidential telemetry")
    assert tenant["cross_tenant_access_blocked"] is True
    assert tenant["sandbox_isolation_verified"] is True

    # 2. Enterprise Identity Protection (MFA Fatigue & Session Hijack)
    identity = EnterpriseIdentityAndTenantArchitecture.analyze_identity_threats("MFA push fatigue attack and session token leak")
    assert identity["mfa_fatigue_bombing_detected"] is True
    assert identity["session_hijacking_suspected"] is True

    # 3. Incident Forensics & Chain of Custody
    custody = IncidentForensicsAndResponse.record_evidence_chain_of_custody("inc_001", "phish email payload", "analyst_john")
    assert "custody_hash" in custody

    # 4. Enterprise Integration Fabric (STIX & Sigma/YARA)
    stix = EnterpriseIntegrationFabric.export_stix_bundle(["https://evil-phish.com"])
    assert len(stix["objects"]) == 1
    rules = EnterpriseIntegrationFabric.generate_sigma_and_yara_rules("Credential-Harvesting", "https://evil-phish.com")
    assert "sigma" in rules and "yara" in rules

    # 5. Cyber Risk Economics & Effectiveness Validation
    econ = SecurityEffectivenessAndEconomics.evaluate_security_effectiveness_and_risk(80.0, 200000.0)
    assert econ["cyber_risk_economics"]["annualized_loss_expectancy_usd"] > 0
    assert econ["security_effectiveness_validation"]["breach_attack_simulation_coverage_pct"] > 90.0

    print("[VERIFIED] PHISHGUARD SOVEREIGN v2.0 APOCALYPSE TIER Acceptance Suite PASSED 100%!")

if __name__ == "__main__":
    test_apocalypse_v2_0_suite()