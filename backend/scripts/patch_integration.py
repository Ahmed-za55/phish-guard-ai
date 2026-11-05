"""One-time integration (safe to run again - it never patches twice, and keeps .bak backups).

  1. backend/app/main.py                          -> registers the real detector (/api/v1/detect)
  2. backend/app/nextgen_core/nextgen_router.py   -> url_risk_score now comes from the trained model
                                                     (a client-supplied score is ignored)
  3. backend/app/nextgen_core/nextgen_dashboard.html and index.html
                                                  -> removes the hardcoded url_risk_score values

Run from anywhere:   python backend/scripts/patch_integration.py
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
APP = ROOT / "backend" / "app"

HELPER = '''
def _resolve_url_risk(req) -> float:
    """URL risk is ALWAYS computed server-side by the trained detector.
    Any url_risk_score sent by a client is ignored (kept in the schema only for old clients)."""
    from fastapi import HTTPException
    from app.real_detector.model import ModelNotAvailable, score_urls
    try:
        return score_urls(req.extracted_urls)
    except ModelNotAvailable as exc:
        raise HTTPException(status_code=503, detail=str(exc))


'''


def backup(path: Path) -> None:
    bak = path.with_suffix(path.suffix + ".bak")
    if not bak.exists():
        shutil.copy2(path, bak)


def patch_main() -> str:
    path = APP / "main.py"
    if not path.exists():
        return "SKIP  backend/app/main.py not found"
    text = path.read_text(encoding="utf-8")
    if "real_detector_router" in text:
        return "OK    main.py already registers the real detector"
    block = (
        "\n# --- real URL detector (trained model) ---\n"
        "from app.real_detector.router import router as real_detector_router\n"
        "app.include_router(real_detector_router)\n"
    )
    m = re.search(r"^if __name__\s*==", text, re.M)
    new = text[: m.start()] + block.lstrip("\n") + "\n" + text[m.start():] if m else text.rstrip("\n") + "\n" + block
    backup(path)
    path.write_text(new, encoding="utf-8")
    return "PATCH main.py -> /api/v1/detect registered"


def patch_nextgen_router() -> str:
    path = APP / "nextgen_core" / "nextgen_router.py"
    if not path.exists():
        return "SKIP  nextgen_router.py not found"
    text = path.read_text(encoding="utf-8")
    if "_resolve_url_risk" in text:
        return "OK    nextgen_router.py already patched"

    new = text
    if not re.search(r"from typing import[^\n]*\bOptional\b", new):
        new = re.sub(r"(from typing import [^\n]+)", r"\1, Optional", new, count=1)
    new, n1 = re.subn(
        r"url_risk_score:\s*float\s*=\s*Field\(default=[\d.]+\)",
        'url_risk_score: Optional[float] = Field(default=None, description="Ignored: computed server-side by the trained URL detector")',
        new,
    )
    new, n2 = re.subn(r"url_risk_score\s*=\s*req\.url_risk_score\s*,", "url_risk_score=_resolve_url_risk(req),", new)
    new, n3 = re.subn(r'(@router\.post\("/analyze"\))', lambda m: HELPER.lstrip("\n") + m.group(1), new, count=1)
    if not (n1 and n2 and n3):
        return ("WARN  nextgen_router.py has a different shape than expected - not modified. "
                "Make url_risk_score Optional and fill it with app.real_detector.model.score_urls(extracted_urls).")
    backup(path)
    path.write_text(new, encoding="utf-8")
    return "PATCH nextgen_router.py -> url_risk_score computed by the trained model"


def strip_fake_scores(path: Path, label: str, also_urls: bool) -> str:
    if not path.exists():
        return f"SKIP  {label} not found"
    text = path.read_text(encoding="utf-8")
    new, removed = re.subn(r"^[ \t]*url_risk_score:[^\n]*\n", "", text, flags=re.M)
    if also_urls:
        js = "extracted_urls: (document.getElementById('inp-msg').value.match(/https?:\\/\\/[^\\s\"'<>]+/g) || []),"
        new = re.sub(
            r'extracted_urls:\s*\[\s*"https://portal-check-node\.org"\s*\]\s*,',
            lambda _m: js,  # lambda: the replacement contains backslashes that re.sub would treat as escapes
            new,
        )
    if new == text:
        return f"OK    {label} has no hardcoded url_risk_score"
    backup(path)
    path.write_text(new, encoding="utf-8")
    return f"PATCH {label} -> removed {removed} hardcoded url_risk_score line(s)"


def main() -> int:
    results = [
        patch_main(),
        patch_nextgen_router(),
        strip_fake_scores(APP / "nextgen_core" / "nextgen_dashboard.html", "nextgen_dashboard.html", also_urls=True),
        strip_fake_scores(ROOT / "index.html", "index.html", also_urls=False),
    ]
    print("\n".join(results))
    print("\nNext: python -m pytest   (from backend/)   then   uvicorn app.main:app --reload")
    return 1 if any(r.startswith("WARN") for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
