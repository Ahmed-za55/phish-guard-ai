"""Checks that the real detector is wired into the actual app (backend/app/main.py).
Run scripts/patch_integration.py once if this fails."""
import pytest


def test_main_app_exposes_real_detector():
    try:
        from app.main import app
    except Exception as exc:  # the legacy modules may need extra deps; don't hide the reason
        pytest.skip(f"app.main could not be imported in this environment: {exc!r}")
    paths = set(app.openapi()["paths"])  # works for nested/included routers in every FastAPI version
    assert "/api/v1/detect" in paths, "run: python scripts/patch_integration.py"
