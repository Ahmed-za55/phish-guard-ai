import pytest

from app.real_detector import model as detector
from helpers import synthetic_frame
from app.real_detector.training import run_training


@pytest.fixture(scope="session")
def tiny_model_dir(tmp_path_factory):
    from app.real_detector.training import load_dataset

    d = tmp_path_factory.mktemp("model")
    csv = d / "ds.csv"
    synthetic_frame().to_csv(csv, index=False)
    run_training(load_dataset(csv), d)
    return d


@pytest.fixture()
def loaded_tiny_model(tiny_model_dir):
    import joblib

    detector.set_bundle(joblib.load(tiny_model_dir / "url_model.joblib"))
    yield
    detector.set_bundle(None)
