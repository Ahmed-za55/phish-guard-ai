from pathlib import Path
from typing import Dict, Any, List
from app.apex_leviathan_v16.leviathan_1_nash_game_solver import GameTheoreticNashSolver
from app.apex_leviathan_v16.leviathan_2_merkle_zk_proof import ZeroKnowledgeMerkleAuditEngine
from app.apex_leviathan_v16.leviathan_3_spectral_laplacian import SpectralGraphCampaignAnalyzer
from app.apex_leviathan_v16.leviathan_4_ast_sentinel import AstSelfIntrospectingSentinel

class ApexLeviathanMasterNexusV16:
    """
    PHISHGUARD SOVEREIGN v16.0 — APEX LEVIATHAN:
    يوحد محرك توازن ناش (Game Theory)، شجرة ميركل المعمّاة (ZK Merkle Proof)،
    التحليل الطيفي لمصفوفة لابلاس (Spectral Laplacian)، والمدقق البنيوي لشجرة الكود (AST Sentinel).
    """
    @staticmethod
    def run_leviathan_pipeline(
        text: str,
        extracted_urls: List[str],
        url_results: List[Dict[str, Any]],
        entropy_val: float = 4.90
    ) -> Dict[str, Any]:
        max_url_risk = max([float(u.get("risk_score", 0.0)) for u in url_results], default=0.0)
        has_fin = any(w in text.lower() for w in ["iban", "swift", "wire", "invoice", "payment"])

        # 1. Game-Theoretic Nash Equilibrium Solver
        nash_solution = GameTheoreticNashSolver.solve_minimax_equilibrium(
            url_risk=max_url_risk,
            entropy=entropy_val,
            financial_intent=has_fin
        )

        # 2. Zero-Knowledge Merkle Tree & Inclusion Proof
        evidence_leaves = [
            f"dominant_strategy:{nash_solution['dominant_defender_strategy']}",
            f"max_url_risk:{max_url_risk}",
            f"financial_lure:{has_fin}",
            f"urls_count:{len(extracted_urls)}"
        ]
        merkle_bundle = ZeroKnowledgeMerkleAuditEngine.build_tree_and_generate_zk_proof(
            evidence_leaves=evidence_leaves,
            target_leaf_index=0
        )
        zk_verified = ZeroKnowledgeMerkleAuditEngine.verify_zk_inclusion_proof(
            raw_leaf_value=evidence_leaves[0],
            blinding_nonce=merkle_bundle["target_blinding_nonce"],
            audit_path=merkle_bundle["zk_inclusion_audit_path"],
            expected_merkle_root=merkle_bundle["merkle_root_hash"]
        )

        # 3. Spectral Graph Laplacian Botnet Decomposer
        infra_nodes = ["corp_mx", "corp_sso", "corp_portal", "fastflux_ip1", "fastflux_ip2", "shadow_Registrar"]
        infra_edges = [
            (0, 1, 0.95), (1, 2, 0.90), (0, 2, 0.85),  # عنقود البنية الشرعية
            (3, 4, 0.92), (4, 5, 0.88), (3, 5, 0.90),  # عنقود البنية الهجومية المترابطة
            (2, 3, 0.04)                               # جسر ضعيف (Phishing Redirect Link)
        ]
        spectral_analysis = SpectralGraphCampaignAnalyzer.analyze_infrastructure_spectrum(infra_nodes, infra_edges)

        # 4. Self-Introspecting AST Codebase Verifier
        current_dir = Path(__file__).resolve().parent
        ast_audit = AstSelfIntrospectingSentinel.verify_directory_source_ast(current_dir)

        return {
            "leviathan_tier": "PHISHGUARD_SOVEREIGN_v16.0_APEX_LEVIATHAN",
            "project_nash_equilibrium": nash_solution,
            "project_merkle_zk_audit": {**merkle_bundle, "mathematical_inclusion_verified": zk_verified},
            "project_laplacian_spectral": spectral_analysis,
            "project_ast_sentinel": ast_audit
        }