from typing import Dict, Any, List
from app.apocalypse_v2_0.enterprise_fabric import EnterpriseIntegrationFabric
from app.apocalypse_v2_0.incident_response_forensics import IncidentForensicsAndResponse
from app.apocalypse_v2_0.identity_tenant_security import EnterpriseIdentityAndTenantArchitecture
from app.apocalypse_v2_0.validation_economics import SecurityEffectivenessAndEconomics

class ApocalypseTierMasterNexusV2:
    """
    المنسق المركزي لإصدار PHISHGUARD SOVEREIGN v2.0 (Apocalypse Tier):
    يجمع الطبقات العشر (L0-L9) في بيئة مؤسسية متكاملة لخدمة العملاء والربط مع SIEM/SOAR.
    """
    @staticmethod
    def run_apocalypse_enterprise_pipeline(
        text: str,
        extracted_urls: List[str],
        url_results: List[Dict[str, Any]],
        tenant_id: str = "enterprise_tenant_alpha"
    ) -> Dict[str, Any]:
        max_url_risk = max([float(u.get("risk_score", 0.0)) for u in url_results], default=0.0)

        # 1. Tenant Isolation
        tenant_res = EnterpriseIdentityAndTenantArchitecture.enforce_tenant_isolation(tenant_id, text)

        # 2. Identity Protection
        identity_res = EnterpriseIdentityAndTenantArchitecture.analyze_identity_threats(text)

        # 3. Incident Forensics & Custody
        forensic_rec = IncidentForensicsAndResponse.record_evidence_chain_of_custody(
            incident_id=f"inc_{tenant_id}_01", evidence_item=text[:50], collector="phishguard_daemon_v2"
        )

        # 4. Autonomous Incident Response
        composite_risk = max(max_url_risk, identity_res["identity_risk_score"])
        response_res = IncidentForensicsAndResponse.orchestrate_incident_response(composite_risk, ["workstation_01", "mail_inbox_user_a"])

        # 5. Enterprise Integration (SIEM / STIX / Sigma / YARA)
        urls_list = [u.get("url", "") for u in url_results if u.get("url")]
        stix_bundle = EnterpriseIntegrationFabric.export_stix_bundle(urls_list)
        rules = EnterpriseIntegrationFabric.generate_sigma_and_yara_rules("Phishing-Credential-Harvesting", urls_list[0] if urls_list else text[:20])

        # 6. Risk Economics & Validation
        economics_res = SecurityEffectivenessAndEconomics.evaluate_security_effectiveness_and_risk(composite_risk, asset_value_usd=150000.0)

        return {
            "apocalypse_tier_version": "PHISHGUARD_SOVEREIGN_v2.0_APOCALYPSE",
            "multi_tenant_isolation": tenant_res,
            "enterprise_identity_protection": identity_res,
            "incident_forensics_custody": forensic_rec,
            "autonomous_incident_response": response_res,
            "enterprise_integration_fabric": {
                "stix_bundle_exported": True,
                "stix_object_count": len(stix_bundle["objects"]),
                "sigma_rule": rules["sigma"],
                "yara_rule": rules["yara"]
            },
            "cyber_risk_economics_and_validation": economics_res
        }