import sys

sys.path.insert(0, "E:/phish-guard-ai/backend")

from app.main import app
from fastapi.routing import APIRoute

print("\n=== FASTAPI ROUTE AUDIT ===")

routes = []

for route in app.routes:
    if isinstance(route, APIRoute):
        methods = ",".join(sorted(route.methods or []))
        print(f"{methods:15} {route.path}")
        routes.append(route)
    else:
        print("[NON-APIRoute]", type(route).__name__)

print("\n=== SUMMARY ===")
print("Total entries:", len(app.routes))
print("Actual API routes:", len(routes))

required = [
    "/analyze",
    "/analyze-image",
    "/analyze-email",
    "/api/backend/health",
    "/ledger/verify",
]

print("\n=== REQUIRED ENDPOINTS ===")

for path in required:
    exists = any(route.path == path for route in routes)
    print(f"{'PASS' if exists else 'FAIL'} {path}")
