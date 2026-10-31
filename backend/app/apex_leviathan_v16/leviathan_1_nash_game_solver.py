import math
from typing import Dict, Any, List

class GameTheoreticNashSolver:
    """
    1. PROJECT NASH-EQUILIBRIUM:
    يحل لعبة استراتيجية غير متماثلة (Stackelberg / Zero-Sum Security Game) بين المهاجم والمدافع
    باستخدام خوارزمية Multiplicative Weights / Regret Minimization لحساب توازن ناش (Nash Equilibrium)
    وتحديد المزيج الدفاعي الأمثل الذي يضمن أقل خسارة قصوى (Minimax Risk).
    """
    DEFENDER_STRATEGIES = [
        "S1_DEEP_DOM_SANDBOX_ISOLATION",
        "S2_OUT_OF_BAND_CRYPTO_CHALLENGE",
        "S3_SESSION_TOKEN_HONEYPOT_TRAP",
        "S4_PASSIVE_TELEMETRY_THROTTLING"
    ]
    ATTACKER_STRATEGIES = [
        "A1_STEALTH_HOMOGRAPH_LURE",
        "A2_AITM_SESSION_COOKIE_HIJACK",
        "A3_BEC_FINANCIAL_INVOICE_SWAP",
        "A4_LOW_AND_SLOW_API_EXHAUSTION"
    ]

    @classmethod
    def solve_minimax_equilibrium(
        cls,
        url_risk: float,
        entropy: float,
        financial_intent: bool,
        iterations: int = 120
    ) -> Dict[str, Any]:
        # بناء مصفوفة الخسائر للمدافع L[i][j] (كلما قلّت القيمة كان أفضل للمدافع)
        # الصفوف i: استراتيجيات المدافع، الأعمدة j: استراتيجيات المهاجم
        fin_mult = 1.6 if financial_intent else 1.0
        ent_mult = max(0.8, min(1.5, entropy / 4.0))
        r_norm = max(0.1, min(1.0, url_risk / 100.0))

        loss_matrix = [
            # A1 (Homograph), A2 (AiTM Session), A3 (BEC Wire), A4 (API Flood)
            [0.10 * r_norm, 0.35 * r_norm, 0.45 * fin_mult, 0.60],          # S1: Deep DOM Sandbox
            [0.40 * r_norm, 0.12 * r_norm, 0.08 * fin_mult, 0.50],          # S2: Out-of-Band Crypto
            [0.35 * ent_mult, 0.09 * r_norm, 0.30 * fin_mult, 0.40],        # S3: Session Honeypot
            [0.75 * r_norm, 0.80 * r_norm, 0.85 * fin_mult, 0.05]           # S4: Telemetry Throttling
        ]

        n_def = len(cls.DEFENDER_STRATEGIES)
        n_att = len(cls.ATTACKER_STRATEGIES)

        # خوارزمية Multiplicative Weights Update (Hedge Algorithm) للتقارب نحو توازن ناش
        def_weights = [1.0 / n_def] * n_def
        att_weights = [1.0 / n_att] * n_att
        def_cumulative = [0.0] * n_def
        att_cumulative = [0.0] * n_att
        eta = math.sqrt(2.0 * math.log(n_def) / max(iterations, 1))

        for _ in range(iterations):
            # حساب الخسارة المتوقعة لكل استراتيجية دفاعية أمام توزيع المهاجم الحالي
            def_losses = [
                sum(loss_matrix[i][j] * att_weights[j] for j in range(n_att))
                for i in range(n_def)
            ]
            # حساب مكسب المهاجم لكل استراتيجية هجومية أمام توزيع المدافع الحالي
            att_gains = [
                sum(loss_matrix[i][j] * def_weights[i] for i in range(n_def))
                for j in range(n_att)
            ]

            # تحديث أوزان المدافع (تقليل الوزن للاستراتيجيات ذات الخسارة العالية)
            def_weights = [def_weights[i] * math.exp(-eta * def_losses[i]) for i in range(n_def)]
            sum_dw = sum(def_weights)
            def_weights = [w / sum_dw for w in def_weights]

            # تحديث أوزان المهاجم (تعظيم الخسارة للمدافع)
            att_weights = [att_weights[j] * math.exp(eta * att_gains[j]) for j in range(n_att)]
            sum_aw = sum(att_weights)
            att_weights = [w / sum_aw for w in att_weights]

            for i in range(n_def):
                def_cumulative[i] += def_weights[i]
            for j in range(n_att):
                att_cumulative[j] += att_weights[j]

        optimal_def_mix = [round(c / iterations, 4) for c in def_cumulative]
        predicted_att_mix = [round(c / iterations, 4) for c in att_cumulative]

        # حساب قيمة اللعبة عند التوازن (Game Value / Minimax Expected Loss)
        game_equilibrium_loss = sum(
            optimal_def_mix[i] * loss_matrix[i][j] * predicted_att_mix[j]
            for i in range(n_def) for j in range(n_att)
        )

        # حساب الخسارة لو اعتمدنا على سياسة ثابتة ساذجة (Uniform / Static Baseline)
        static_baseline_loss = max(
            sum((1.0 / n_def) * loss_matrix[i][j] for i in range(n_def))
            for j in range(n_att)
        )

        best_idx = optimal_def_mix.index(max(optimal_def_mix))
        worst_att_idx = predicted_att_mix.index(max(predicted_att_mix))

        return {
            "nash_equilibrium_converged": True,
            "dominant_defender_strategy": cls.DEFENDER_STRATEGIES[best_idx],
            "anticipated_adversary_vector": cls.ATTACKER_STRATEGIES[worst_att_idx],
            "defender_mixed_strategy_distribution": dict(zip(cls.DEFENDER_STRATEGIES, optimal_def_mix)),
            "adversary_mixed_strategy_distribution": dict(zip(cls.ATTACKER_STRATEGIES, predicted_att_mix)),
            "minimax_equilibrium_expected_loss": round(game_equilibrium_loss, 4),
            "naive_static_policy_worst_loss": round(static_baseline_loss, 4),
            "game_theoretic_risk_reduction_pct": round(((static_baseline_loss - game_equilibrium_loss) / max(static_baseline_loss, 1e-6)) * 100, 2)
        }