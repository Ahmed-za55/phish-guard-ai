"""Train + evaluate the URL detector.

Run from the backend/ folder:
    python scripts/train.py

Outputs:
    models/url_model.joblib   the model used by the API
    models/metrics.json       all numbers
    docs/RESULTS.md           the results table (also injected into README.md between the RESULTS markers)
"""
import sys
from pathlib import Path

BACKEND = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND))

from app.real_detector.training import load_dataset, results_markdown, run_training, update_readme  # noqa: E402


def main() -> int:
    data_path = BACKEND / "data" / "dataset.csv"
    if not data_path.exists():
        print("Missing data/dataset.csv - run: python scripts/fetch_data.py")
        return 1

    df = load_dataset(data_path)
    print(f"Loaded {len(df):,} unique hosts ({int(df['label'].sum()):,} phishing). Training...")
    report = run_training(
        df, BACKEND / "models",
        dataset_info={"sources": ["Phishing.Database (phishing)", "OpenDNS top domains (legitimate)"]},
    )

    md = results_markdown(report)
    docs = BACKEND.parent / "docs"
    docs.mkdir(exist_ok=True)
    (docs / "RESULTS.md").write_text("# Results\n\n" + md + "\n", encoding="utf-8")
    updated = update_readme(BACKEND.parent / "README.md", md)

    print("\n" + md + "\n")
    print(f"Selected model : {report['selected_model']}")
    print(f"Saved          : models/url_model.joblib, models/metrics.json, docs/RESULTS.md"
          f"{', README.md' if updated else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
