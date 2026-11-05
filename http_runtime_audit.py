import sys
sys.path.insert(0, "E:/phish-guard-ai/backend")

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

tests = [
    ("GET", "/"),
    ("GET", "/health"),
    ("GET", "/api/backend/health"),
    ("GET", "/api/backend/"),
    ("GET", "/openapi.json"),
]

print("\n=== HTTP RUNTIME TEST ===")

for method, path in tests:
    try:
        response = client.request(method, path)
        print(
            f"{method:6} {path:25} "
            f"STATUS={response.status_code}"
        )
        print("BODY:", response.text[:250].replace("\n", " "))
    except Exception as exc:
        print(f"ERROR {method} {path}: {type(exc).__name__}: {exc}")

