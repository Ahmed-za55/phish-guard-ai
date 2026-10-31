from typing import Dict, Any, List

class CivilizationAndFailureIntelligence:
    """
    الركيزة الرابعة المساندة (Capabilities 1, 2, 4, 6, 7):
    - Digital Civilization Attack Intelligence: تحليل انتقال العدوى عبر سلاسل التوريد ومزودي الهوية.
    - Cyber Failure Prediction: اكتشاف هشاشة البيئة قبل وقوع الهجوم (SPOF, Expiring Certs, Excessive Privs).
    - Digital Trust Negotiation Protocol: منح ثقة ديناميكية بأقل صلاحية ووقت انتهاء محدد.
    """
    @staticmethod
    def analyze_civilization_cascade_and_fragility(
        dependency_graph: Dict[str, List[str]],
        compromised_provider: str,
        cert_days_remaining: int,
        single_provider_dependencies: List[str]
    ) -> Dict[str, Any]:
        # BFS لاكتشاف جميع المؤسسات والخدمات المتأثرة بالتسلسل
        visited = set()
        queue = [compromised_provider]
        while queue:
            curr = queue.pop(0)
            for consumer, providers in dependency_graph.items():
                if curr in providers and consumer not in visited:
                    visited.add(consumer)
                    queue.append(consumer)

        fragility_triggers = []
        if cert_days_remaining <= 7:
            fragility_triggers.append(f"CRITICAL_CERT_EXPIRY_IN_{cert_days_remaining}_DAYS")
        if single_provider_dependencies:
            fragility_triggers.append(f"SINGLE_POINT_OF_FAILURE_PROVIDERS:{','.join(single_provider_dependencies)}")

        pre_attack_failure_probability = min(0.99, round(0.25 * len(fragility_triggers) + 0.15 * len(visited), 3))

        return {
            "initial_compromised_provider": compromised_provider,
            "cascading_impacted_organizations": sorted(list(visited)),
            "blast_radius_count": len(visited),
            "structural_fragility_triggers": fragility_triggers,
            "pre_attack_failure_probability": pre_attack_failure_probability
        }

    @staticmethod
    def negotiate_dynamic_trust_lease(
        peer_id: str,
        identity_proof_verified: bool,
        source_reliability: float,
        requested_permissions: List[str],
        minimum_required_permissions: List[str]
    ) -> Dict[str, Any]:
        if (not identity_proof_verified) or source_reliability < 0.60:
            return {
                "peer_id": peer_id,
                "trust_granted": False,
                "granted_permissions": [],
                "lease_ttl_seconds": 0,
                "revocation_reason": "INSUFFICIENT_IDENTITY_OR_REPUTATION_PROOF"
            }

        # منح أقل صلاحيات لازمة فقط (Least Privilege Intersection)
        granted = [p for p in requested_permissions if p in minimum_required_permissions]
        return {
            "peer_id": peer_id,
            "trust_granted": True,
            "granted_permissions": granted,
            "Excess_permissions_stripped": [p for p in requested_permissions if p not in granted],
            "lease_ttl_seconds": 300
        }