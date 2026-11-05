import sys
sys.path.insert(0, "E:/phish-guard-ai/backend")

from app.main import app

def inspect_routes(router, prefix=""):
    for route in router.routes:
        path = getattr(route, "path", None)

        if path is not None:
            methods = sorted(getattr(route, "methods", []) or [])
            print(f"{','.join(methods):15} {prefix}{path}")

        elif hasattr(route, "routes"):
            print(f"\n[NESTED ROUTER] {type(route).__name__}")
            inspect_routes(route, prefix)

print("=== COMPLETE ROUTE TREE ===")
inspect_routes(app)

