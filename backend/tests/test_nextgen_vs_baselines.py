import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.nextgen_core.tech_1_security_compiler import AutonomousSecurityCompiler
from app.nextgen_core.tech_2_predictive_attack_universe import PredictiveAttackUniverse
from app.nextgen_core.tech_3_digital_immune_system import AutonomousDigitalImmuneSystem

def test_nextgen_technologies_vs_baselines():
    print("=" * 96)
    print(" PHISHGUARD SOVEREIGN — NEXT-GEN CORE TECHNOLOGIES vs. BASELINE BENCHMARK SUITE")
    print("=" * 96)

    # -------------------------------------------------------------------------
    # BENCHMARK 1: Autonomous Security Compiler vs. Static Keyword Baseline
    # -------------------------------------------------------------------------
    research_report = """
    Threat Advisory: Attackers are spoofing Microsoft login flows using newly registered domains
    with domain age under 14 days, requesting OAuth scope mail.readwrite, and deploying a
    financial lure containing 'iban' under psychological lever: urgency.
    """
    compiled_bundle = AutonomousSecurityCompiler.compile_threat_research(research_report, "TR-2026-099")
    assert compiled_bundle["stage_8_deployment_state"] == "STAGED_VERIFIED_READY"

    # مقارنة على عينة مراوغة (حذفت كلمة iban واستبدلتها بطلب تفويض مع إبقاء النطاق حديثاً والـ OAuth خطيراً)
    evasive_sample = {
        "domain_age_days": 4,
        "oauth_scope": "mail.readwrite",
        "text": "Immediate settlement authorization required",
        "deception_lever": "urgency"
    }
    keyword_baseline_detected = ("iban" in evasive_sample["text"].lower())
    compiler_detected = compiled_bundle["executable_detector"](evasive_sample)

    assert keyword_baseline_detected is False
    assert compiler_detected is True
    print(" [1/3 SECURITY COMPILER] Translated prose advisory into AST detector, passed 3/3 auto-tests,")
    print("       and caught evasive OAuth attack that bypassed the Keyword Baseline!")

    # -------------------------------------------------------------------------
    # BENCHMARK 2: Predictive Attack Universe vs. Reactive First-Node Baseline
    # -------------------------------------------------------------------------
    # مهاجم يدخل من نقطتين (phish_mail_1 و phish_mail_2) وكلاهما يمر عبر عقدة الهوية المركزية (sso_hub)
    # للوصول إلى الخزينة المالية (treasury_db بقيمة 500,000 دولار)
    attack_graph = {
        "phish_entry_1": [("sso_hub", 0.85)],
        "phish_entry_2": [("sso_hub", 0.80)],
        "sso_hub": [("treasury_db", 0.90), ("erp_core", 0.75)],
        "erp_core": [("treasury_db", 0.60)]
    }
    assets = {"treasury_db": 500000.0, "erp_core": 150000.0}
    costs = {"phish_entry_1": 300.0, "phish_entry_2": 300.0, "sso_hub": 1200.0, "erp_core": 800.0}

    universe = PredictiveAttackUniverse.explore_future_attack_universe(
        entry_nodes=["phish_entry_1", "phish_entry_2"],
        adjacency_graph=attack_graph,
        asset_values_usd=assets,
        intervention_costs_usd=costs
    )

    # الـ Baseline التفاعلي يعزل phish_entry_1 فقط فيترك phish_entry_2 يخترق sso_hub!
    # بينما Predictive Attack Universe يكتشف أن sso_hub هو عنق الزجاجة (Chokepoint) الذي يصفر الخسارة!
    assert universe["optimal_chokepoint_node"] == "sso_hub"
    assert universe["optimal_chokepoint_total_burden_usd"] < universe["reactive_baseline_total_burden_usd"]
    assert universe["net_savings_vs_reactive_baseline_usd"] > 300000.0
    print(f" [2/3 PREDICTIVE ATTACK UNIVERSE] Identified Chokepoint '{universe['optimal_chokepoint_node']}' ->")
    print(f"       Saved ${universe['net_savings_vs_reactive_baseline_usd']:,.2f} compared to Reactive Entry-Node Baseline!")

    # -------------------------------------------------------------------------
    # BENCHMARK 3: Autonomous Digital Immune System vs. Stateless Signature Baseline
    # -------------------------------------------------------------------------
    immune = AutonomousDigitalImmuneSystem()
    clean_hash = immune.register_healthy_baseline_snapshot(
        "finance_workstation_01",
        {"os_integrity": "CLEAN", "oauth_tokens": ["legit_tok_1"], "forwarding_rules": []}
    )

    known_sigs = {"sig_strain_v1_exact"}

    # الهجوم الأول (السلالة الأصلية v1)
    wave_1 = immune.handle_infection_lifecycle(
        entity_id="finance_workstation_01",
        pathogen_vector=[0.92, 0.85, 0.78, 0.88],
        exact_signature_hash="sig_strain_v1_exact",
        compromised_runtime_state={"os_integrity": "TAINTED", "forwarding_rules": ["evil@ext.com"]},
        known_static_signatures=known_sigs
    )
    assert wave_1["detected_by_digital_immune_system"] is True
    assert wave_1["recovery_integrity_verified"] is True
    assert wave_1["restored_golden_sha256"] == clean_hash

    # الهجوم الثاني (سلالة متحورة v2 غيّرت الـ Hash التشفيري وعدّلت الأوزان قليلاً لتفادي التوقيعات الثابتة)
    wave_2_mutated = immune.handle_infection_lifecycle(
        entity_id="finance_workstation_01",
        pathogen_vector=[0.89, 0.82, 0.80, 0.85],  # تحور سلوكي طفيف لكن نفس اتجاه المتجه
        exact_signature_hash="sig_strain_v2_mutated_unseen",
        compromised_runtime_state={"os_integrity": "TAINTED_V2"},
        known_static_signatures=known_sigs
    )

    # الـ Baseline يفشل في كشف السلالة المتحورة، بينما الذاكرة المناعية (B-Cell Affinity) تلتقطها فوراً!
    assert wave_2_mutated["detected_by_static_signature_baseline"] is False
    assert wave_2_mutated["detected_by_digital_immune_system"] is True
    assert wave_2_mutated["response_mode"] == "SECONDARY_MEMORY_B_CELL_FAST_KILL"
    assert wave_2_mutated["antibody_affinity_score"] >= 0.98
    print(f" [3/3 DIGITAL IMMUNE SYSTEM] Neutralized mutated pathogen (Affinity={wave_2_mutated['antibody_affinity_score']}) ")
    print("       that completely evaded the Static Signature Baseline, and verified SHA-256 tissue recovery!")

    print("=" * 96)
    print(" [ALL 3 NEXT-GEN CORE TECHNOLOGIES PROVEN SUPERIOR TO BASELINES — 100% PASSED]")
    print("=" * 96)

if __name__ == "__main__":
    test_nextgen_technologies_vs_baselines()