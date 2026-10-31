import json
import hashlib
from typing import Dict, Any, List

class EnterpriseIntegrationFabric:
    """
    L7 — Enterprise Integration Fabric:
    يتكامل مع SIEM/SOAR، يصدر حزم STIX/TAXII، ويولد قواعد Sigma و YARA للاستجابة المؤسسية.
    """
    @staticmethod
    def export_stix_bundle(threat_indicators: List[str], campaign_name: string = "Enterprise-PhishCampaign") -> Dict[str, Any]:
        stix_objects = []
        for ind in threat_indicators:
            obj_id = f"indicator--{hashlib.sha256(ind.encode()).hexdigest()[:16]}"
            stix_objects.append({
                "type": "indicator",
                "spec_version": "2.1",
                "id": obj_id,
                "pattern": f"[url:value = '{ind}']",
                "valid_from": "2026-01-01T00:00:00Z",
                "labels": ["malicious-activity", campaign_name]
            })
        return {
            "type": "bundle",
            "id": f"bundle--{hashlib.sha256(campaign_name.encode()).hexdigest()[:16]}",
            "objects": stix_objects
        }

    @staticmethod
    def generate_sigma_and_yara_rules(threat_type: str, indicator_value: str) -> Dict[str, str]:
        sigma_rule = f"""
title: Detection of Enterprise Phishing via {threat_type}
status: experimental
level: high
logsource:
  category: proxy
  product: web_gateway
detection:
  selection:
    uri: '{indicator_value}'
  condition: selection
        """.strip()

        yara_rule = f"""
rule enterprise_phish_{hashlib.sha256(indicator_value.encode()).hexdigest()[:8]} {{
    meta:
        description = "Detects malicious enterprise threat pattern for {threat_type}"
        author = "PhishGuard Sovereign v2.0"
    strings:
        $s1 = "{indicator_value}" ascii wide
    condition:
        any of them
}}
        """.strip()

        return {"sigma": sigma_rule, "yara": yara_rule}