import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.infinity_dominion_v11.dominion_router import serve_sovereign_7_plane_dashboard

def test_dashboard_endpoint():
    resp = serve_sovereign_7_plane_dashboard()
    assert resp.status_code == 200
    assert "PHISHGUARD SOVEREIGN — INFINITY DOMINION v11.0" in resp.body.decode("utf-8")
    assert "/api/v1/dominion/analyze" in resp.body.decode("utf-8")
    print("[DASHBOARD VERIFIED] Sovereign 7-Plane Command Dashboard HTML & API Wiring PASSED 100%!")

if __name__ == "__main__":
    test_dashboard_endpoint()