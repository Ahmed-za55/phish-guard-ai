import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.real_detector import model as detector
from app.real_detector.router import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)

PHISH = "http://secure-login-verify-48213-garden.xyz/verify"
LEGIT = "https://www.pizzagarden.com/menu"


def test_detect_returns_expected_fields(loaded_tiny_model):
    r = client.post("/api/v1/detect", json={"url": PHISH})
    assert r.status_code == 200
    d = r.json()
    for key in ("host", "scored_domain", "probability", "risk_score", "verdict", "indicators", "model"):
        assert key in d
    assert 0 <= d["probability"] <= 1 and d["risk_score"] == round(d["probability"] * 100, 1)


def test_score_depends_on_the_url(loaded_tiny_model):
    bad = client.post("/api/v1/detect", json={"url": PHISH}).json()
    good = client.post("/api/v1/detect", json={"url": LEGIT}).json()
    assert bad["risk_score"] > good["risk_score"]
    assert bad["verdict"] == "PHISHING" and good["verdict"] == "LIKELY_SAFE"


def test_subdomain_and_path_do_not_change_the_score(loaded_tiny_model):
    a = client.post("/api/v1/detect", json={"url": "https://pizzagarden.com"}).json()
    b = client.post("/api/v1/detect", json={"url": "https://mail.pizzagarden.com/a/b?c=d"}).json()
    assert a["risk_score"] == b["risk_score"] and b["scored_domain"] == "pizzagarden.com"


@pytest.mark.parametrize("payload", [{}, {"url": ""}, {"url": "   "}, {"url": "javascript:alert(1)"}])
def test_invalid_input_is_rejected(loaded_tiny_model, payload):
    assert client.post("/api/v1/detect", json=payload).status_code == 422


def test_missing_model_gives_503_not_a_fake_score(monkeypatch, tmp_path):
    detector.set_bundle(None)
    monkeypatch.setenv("PHISHGUARD_MODEL", str(tmp_path / "nope.joblib"))
    r = client.post("/api/v1/detect", json={"url": PHISH})
    assert r.status_code == 503
    assert client.get("/api/v1/detect/health").json()["status"] == "model_missing"


def test_health_and_ui(loaded_tiny_model):
    assert client.get("/api/v1/detect/health").json()["status"] == "ok"
    ui = client.get("/api/v1/detect/ui")
    assert ui.status_code == 200 and "/api/v1/detect" in ui.text
    assert "85.0" not in ui.text  # the old hardcoded fake score must never come back


def test_score_urls_takes_the_max_and_ignores_junk(loaded_tiny_model):
    assert detector.score_urls([]) == 0.0
    assert detector.score_urls(["javascript:alert(1)"]) == 0.0
    both = detector.score_urls([LEGIT, PHISH])
    assert both == detector.score_urls([PHISH]) > detector.score_urls([LEGIT])


def test_shared_hosting_is_not_scored(loaded_tiny_model):
    d = client.post("/api/v1/detect", json={"url": "https://my-site.netlify.app"}).json()
    assert d["verdict"] == "NOT_SCORED" and d["risk_score"] is None
    assert any("shared platform" in h for h in d["indicators"])
    assert detector.score_urls(["https://my-site.netlify.app"]) == 0.0
