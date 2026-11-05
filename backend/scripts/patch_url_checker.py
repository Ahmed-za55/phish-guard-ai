"""Feed the trained domain model into the existing rule engine (backend/app/services/url_checker.py).

Policy (kept deliberately simple):
  model says PHISHING    -> url score = max(rule score, model score)
  model says SUSPICIOUS  -> url score + 10
  model unavailable / shared hosting (NOT_SCORED) -> rules behave exactly as before
The model never lowers a score. A .bak copy is kept. Safe to run twice.

Run:  python backend/scripts/patch_url_checker.py
"""
import re
import shutil
import sys
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "app" / "services" / "url_checker.py"

HELPER = '''def _trained_model_signal(hostname: str):
    """(verdict, score) from the trained domain model, or None when unavailable / not scorable."""
    if not hostname:
        return None
    try:
        from app.real_detector.model import analyze_url as model_analyze
        result = model_analyze("http://" + hostname)
    except Exception:
        return None
    if result.get("verdict") in (None, "NOT_SCORED") or result.get("risk_score") is None:
        return None
    return result["verdict"], int(round(result["risk_score"]))


'''

BLOCK = '''    model_signal = _trained_model_signal(hostname)
    if model_signal:
        model_verdict, model_score = model_signal
        if model_verdict == "PHISHING":
            score = max(score, model_score)
            reasons.append(f"Trained domain model: high-risk domain (model score {model_score}/100).")
        elif model_verdict == "SUSPICIOUS":
            score += 10
            reasons.append(f"Trained domain model: suspicious domain (model score {model_score}/100).")

'''


def main() -> int:
    if not PATH.exists():
        print(f"SKIP  {PATH} not found")
        return 0
    text = PATH.read_text(encoding="utf-8")
    if "_trained_model_signal" in text:
        print("OK    url_checker.py already uses the trained model")
        return 0
    new, n1 = re.subn(r"^def analyze_url\(", lambda m: HELPER + m.group(0), text, count=1, flags=re.M)
    new, n2 = re.subn(r"^    score = min\(score, 100\)\n", lambda m: BLOCK + m.group(0), new, count=1, flags=re.M)
    if not (n1 and n2):
        print("WARN  url_checker.py has a different shape than expected - not modified")
        return 1
    shutil.copy2(PATH, PATH.with_suffix(".py.bak"))
    PATH.write_text(new, encoding="utf-8")
    print("PATCH url_checker.py -> trained model feeds the URL score")
    return 0


if __name__ == "__main__":
    sys.exit(main())
