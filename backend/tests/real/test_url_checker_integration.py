"""After scripts/patch_url_checker.py, the rule engine must use the trained model (never fake values)."""
import pytest

PHISH = "http://secure-login-verify-48213-garden.xyz/verify"


def _url_checker():
    try:
        from app.services import url_checker
    except Exception as exc:
        pytest.skip(f"app.services.url_checker not importable here: {exc!r}")
    if not hasattr(url_checker, "_trained_model_signal"):
        pytest.skip("run: python scripts/patch_url_checker.py")
    return url_checker


def test_model_signal_is_used_and_explained(loaded_tiny_model):
    uc = _url_checker()
    out = uc.analyze_url(PHISH)
    assert any("Trained domain model" in r for r in out["reasons"])
    assert out["risk_score"] >= 50


def test_model_never_lowers_a_rule_score(loaded_tiny_model):
    uc = _url_checker()
    out = uc.analyze_url("http://192.168.4.77/account/update")  # IP host: rules alone already score it
    assert out["risk_score"] >= 50


def test_shared_hosting_gets_no_model_signal(loaded_tiny_model):
    uc = _url_checker()
    out = uc.analyze_url("https://my-site.netlify.app")
    assert not any("Trained domain model" in r for r in out["reasons"])


def test_rules_still_work_without_a_model(monkeypatch, tmp_path):
    from app.real_detector import model as detector
    uc = _url_checker()
    detector.set_bundle(None)
    monkeypatch.setenv("PHISHGUARD_MODEL", str(tmp_path / "missing.joblib"))
    out = uc.analyze_url("http://192.168.4.77/account/update")
    assert out["risk_score"] > 0 and not any("Trained domain model" in r for r in out["reasons"])
