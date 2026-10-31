import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.apex_leviathan_v16.leviathan_1_nash_game_solver import GameTheoreticNashSolver
from app.apex_leviathan_v16.leviathan_2_merkle_zk_proof import ZeroKnowledgeMerkleAuditEngine
from app.apex_leviathan_v16.leviathan_3_spectral_laplacian import SpectralGraphCampaignAnalyzer
from app.apex_leviathan_v16.leviathan_4_ast_sentinel import AstSelfIntrospectingSentinel
from app.apex_leviathan_v16.leviathan_master import ApexLeviathanMasterNexusV16

def test_apex_leviathan_v16_suite():
    print("=" * 90)
    print(" PHISHGUARD SOVEREIGN v16.0 (APEX LEVIATHAN) — HARDCORE ALGORITHMIC VERIFICATION")
    print("=" * 90)

    # 1. Test Nash Equilibrium Game Solver
    nash = GameTheoreticNashSolver.solve_minimax_equilibrium(url_risk=92.0, entropy=5.1, financial_intent=True)
    assert nash["nash_equilibrium_converged"] is True
    assert nash["minimax_equilibrium_expected_loss"] < nash["naive_static_policy_worst_loss"]
    assert abs(sum(nash["defender_mixed_strategy_distribution"].values()) - 1.0) < 0.01
    print(f" [1/4 NASH EQUILIBRIUM] Converged! Dominant Strategy: {nash['dominant_defender_strategy']} "
          f"(Risk Reduced by {nash['game_theoretic_risk_reduction_pct']}% vs Static Policy)")

    # 2. Test Zero-Knowledge Merkle Inclusion Proof & Tamper Rejection
    leaves = ["ev_domain:evil.org", "ev_asn:AS666", "ev_dom:password_trap", "ev_tls:self_signed"]
    proof_bundle = ZeroKnowledgeMerkleAuditEngine.build_tree_and_generate_zk_proof(leaves, target_leaf_index=2)
    valid_proof = ZeroKnowledgeMerkleAuditEngine.verify_zk_inclusion_proof(
        raw_leaf_value="ev_dom:password_trap",
        blinding_nonce=proof_bundle["target_blinding_nonce"],
        audit_path=proof_bundle["zk_inclusion_audit_path"],
        expected_merkle_root=proof_bundle["merkle_root_hash"]
    )
    tampered_proof = ZeroKnowledgeMerkleAuditEngine.verify_zk_inclusion_proof(
        raw_leaf_value="ev_dom:benign_page",
        blinding_nonce=proof_bundle["target_blinding_nonce"],
        audit_path=proof_bundle["zk_inclusion_audit_path"],
        expected_merkle_root=proof_bundle["merkle_root_hash"]
    )
    assert valid_proof is True
    assert tampered_proof is False
    print(f" [2/4 MERKLE-ZK PROOF] Inclusion Proof Verified (Root={proof_bundle['merkle_root_hash'][:20]}...) & Tamper Rejected!")

    # 3. Test Spectral Graph Laplacian Botnet Partitioning
    nodes = ["legit_1", "legit_2", "legit_3", "botnet_a", "botnet_b", "botnet_c"]
    edges = [(0, 1, 1.0), (1, 2, 1.0), (0, 2, 1.0), (3, 4, 1.0), (4, 5, 1.0), (3, 5, 1.0), (2, 3, 0.02)]
    spec = SpectralGraphCampaignAnalyzer.analyze_infrastructure_spectrum(nodes, edges)
    assert spec["coordinated_botnet_cluster_detected"] is True
    assert set(spec["spectral_partition_alpha"]) in [{"legit_1", "legit_2", "legit_3"}, {"botnet_a", "botnet_b", "botnet_c"}]
    print(f" [3/4 LAPLACIAN SPECTRAL] Fiedler Value={spec['fiedler_algebraic_connectivity']} -> Isolated Botnet Partition: {spec['spectral_partition_beta']}")

    # 4. Test Self-Introspecting AST Sentinel on Live Codebase
    target_dir = Path("E:/phish-guard-ai/backend/app/apex_leviathan_v16")
    ast_res = AstSelfIntrospectingSentinel.verify_directory_source_ast(target_dir)
    assert ast_res["ast_introspection_verified"] is True
    assert len(ast_res["security_violations_found"]) == 0
    print(f" [4/4 AST-SENTINEL] Parsed {ast_res['total_ast_nodes_parsed']} AST nodes across {ast_res['files_inspected_count']} files -> 0 Violations!")

    # Full Master Pipeline
    master_res = ApexLeviathanMasterNexusV16.run_leviathan_pipeline(
        text="URGENT: Swift IBAN invoice wire transfer required immediately",
        extracted_urls=["https://fastflux-login.net"],
        url_results=[{"url": "https://fastflux-login.net", "risk_score": 94.0}]
    )
    assert master_res["project_merkle_zk_audit"]["mathematical_inclusion_verified"] is True

    print("=" * 90)
    print(" [100% VERIFIED] PHISHGUARD SOVEREIGN v16.0 (APEX LEVIATHAN) ALL ALGORITHMS PASSED!")
    print("=" * 90)

if __name__ == "__main__":
    test_apex_leviathan_v16_suite()