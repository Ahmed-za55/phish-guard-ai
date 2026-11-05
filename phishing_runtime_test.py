import sys
import json

sys.path.insert(0, "E:/phish-guard-ai/backend")

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

payload = {
    "text": "URGENT: Your bank account has been suspended. Verify your identity immediately at http://secure-bank-login.example.com to restore access."
}

print("\n=== PHISHING ANALYSIS TEST ===")

try:
    response = client.post("/analyze", json=payload)

    print("HTTP STATUS:", response.status_code)
    print("RESPONSE:")

    try:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except Exception:
        print(response.text[:3000])

except Exception as exc:
    print("EXCEPTION:", type(exc).__name__, str(exc))
