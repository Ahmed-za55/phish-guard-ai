import math
from typing import Dict, Any, List, Tuple

class SpectralGraphCampaignAnalyzer:
    """
    3. PROJECT LAPLACIAN-SPECTRAL:
    يبني مصفوفة لابلاس المعيّرة (Normalized Graph Laplacian) لشبكة البنية التحتية
    ويستخدم طريقة القوى المتعامدة (Deflated Power Iteration) لاستخراج القيم الذاتية
    (Eigenvalues) واكتشاف تجمعات البنية الخبيثة المعزولة (Botnet / Fast-Flux Clusters).
    """
    @staticmethod
    def analyze_infrastructure_spectrum(
        nodes: List[str],
        edges: List[Tuple[int, int, float]]
    ) -> Dict[str, Any]:
        n = len(nodes)
        if n < 2:
            return {"spectral_gap": 0.0, "coordinated_botnet_detected": False}

        # بناء مصفوفة التجاور الموزونة A ومصفوفة الدرجات D
        adj = [[0.0] * n for _ in range(n)]
        for u, v, w in edges:
            if 0 <= u < n and 0 <= v < n and u != v:
                adj[u][v] = w
                adj[v][u] = w

        degrees = [sum(adj[i]) for i in range(n)]
        inv_sqrt_deg = [1.0 / math.sqrt(d) if d > 1e-9 else 0.0 for d in degrees]

        # حساب مصفوفة الترابط المعيّرة M = D^(-1/2) A D^(-1/2)
        # القيم الذاتية لـ L_norm = I - M تقع في [0, 2]
        m_mat = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                m_mat[i][j] = adj[i][j] * inv_sqrt_deg[i] * inv_sqrt_deg[j]

        # المتجه الذاتي الأول لـ M مرتبط بـ sqrt(degrees) (القيمة الذاتية الكبرى = 1)
        v0 = [math.sqrt(max(d, 1e-9)) for d in degrees]
        norm_v0 = math.sqrt(sum(x * x for x in v0)) or 1.0
        v0 = [x / norm_v0 for x in v0]

        # إيجاد المتجه الذاتي الثاني لـ M (المقابل لمتجه Fiedler في مصفوفة لابلاس) عبر Deflated Power Iteration
        vec = [((i * 17 + 5) % 11) - 5.0 for i in range(n)]
        for _ in range(45):
            # إزالة المركبة الموازية لـ v0 (Orthogonal Deflation)
            dot_v0 = sum(vec[i] * v0[i] for i in range(n))
            vec = [vec[i] - dot_v0 * v0[i] for i in range(n)]

            # ضرب المصفوفة M * vec
            nxt = [sum(m_mat[i][j] * vec[j] for j in range(n)) for i in range(n)]
            norm_nxt = math.sqrt(sum(x * x for x in nxt)) or 1e-9
            vec = [x / norm_nxt for x in nxt]

        # حساب حاصل رايلي (Rayleigh Quotient) للحصول على القيمة الذاتية الثانية لـ M
        m_vec = [sum(m_mat[i][j] * vec[j] for j in range(n)) for i in range(n)]
        lambda_2_m = sum(vec[i] * m_vec[i] for i in range(n))

        # القيمة الذاتية الثانية لمصفوفة لابلاس (Algebraic Connectivity / Fiedler Value)
        fiedler_eigenvalue = max(0.0, min(2.0, round(1.0 - lambda_2_m, 4)))

        # تقسيم العقد إلى مجموعتين بناءً على إشارة متجه Fiedler
        cluster_positive = [nodes[i] for i in range(n) if vec[i] >= 0]
        cluster_negative = [nodes[i] for i in range(n) if vec[i] < 0]

        # وجود فجوة طيفية صغيرة مع انقسام واضح يعني وجود عنقود هجومي شبه معزول (Modular Botnet Cluster)
        coordinated_cluster_detected = (0.001 < fiedler_eigenvalue < 0.45) and len(cluster_positive) >= 2 and len(cluster_negative) >= 2

        return {
            "fiedler_algebraic_connectivity": fiedler_eigenvalue,
            "second_markov_eigenvalue": round(lambda_2_m, 4),
            "coordinated_botnet_cluster_detected": coordinated_cluster_detected,
            "spectral_partition_alpha": cluster_positive,
            "spectral_partition_beta": cluster_negative
        }