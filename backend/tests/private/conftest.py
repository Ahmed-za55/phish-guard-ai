import pytest

from app.privacy_gateway import provider as provider_module
from app.privacy_gateway import service
from app.privacy_gateway.provider import MockProvider


@pytest.fixture(autouse=True)
def clean_state(monkeypatch, tmp_path):
    monkeypatch.setattr(provider_module, "ENV_FILE", tmp_path / "no-such.env")  # never read the real backend/.env
    monkeypatch.setenv("PRIVATE_PROVIDER", "mock")
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    service.reset_sessions()
    yield
    service.reset_sessions()


@pytest.fixture()
def spy():
    return MockProvider()
