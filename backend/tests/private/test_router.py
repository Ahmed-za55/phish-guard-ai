from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.privacy_gateway import router as router_module

app = FastAPI()
app.include_router(router_module.router)
client = TestClient(app)

BODY = {"text": "Hi Mariam Hassan, verify at http://secure-login-48213.xyz/verify mail a@b.co", "protected_terms": ["Mariam Hassan"]}


def setup_function():
    router_module._calls.clear()


def test_analyze_and_restore_flow():
    r = client.post("/api/v1/private/analyze", json=BODY)
    assert r.status_code == 200
    data = r.json()
    assert "Mariam Hassan" not in data["sanitized_text"] and "a@b.co" not in data["sanitized_text"]
    assert data["provider"]["name"] == "mock"
    shares = [s["share"] for s in data["custody"]["shares"]]
    one = client.post("/api/v1/private/restore", json={"request_id": data["request_id"], "shares": shares[:1]})
    assert one.status_code == 403
    two = client.post("/api/v1/private/restore", json={"request_id": data["request_id"], "shares": shares[:2]})
    assert two.status_code == 200 and two.json()["restored"] is True


def test_validation_errors():
    assert client.post("/api/v1/private/analyze", json={"text": ""}).status_code == 422
    assert client.post("/api/v1/private/analyze", json={"text": "x" * 9000}).status_code == 422
    assert client.post("/api/v1/private/analyze", json={"text": "hi", "protected_terms": ["a"] * 25}).status_code == 422
    assert client.post("/api/v1/private/restore", json={"request_id": "zzzz1234", "shares": ["PG1.x"]}).status_code == 404


def test_rate_limit():
    codes = [client.post("/api/v1/private/analyze", json={"text": "hello there"}).status_code for _ in range(25)]
    assert codes.count(200) == router_module._MAX_CALLS and codes[-1] == 429


def test_status_reports_the_provider():
    assert client.get("/api/v1/private/status").json()["provider"] == "mock"


def test_selftest_passes_over_http():
    data = client.get("/api/v1/private/selftest").json()
    assert data["passed"] == data["total"] == 10, [c for c in data["checks"] if not c["passed"]]
