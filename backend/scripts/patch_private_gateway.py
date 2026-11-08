"""Register the private-analysis router in backend/app/main.py (safe to run twice, keeps a .bak copy).

Run:  python backend/scripts/patch_private_gateway.py
"""
import re
import shutil
import sys
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "app" / "main.py"
BLOCK = (
    "\n# --- private analysis (tokenization + AES-256-GCM vault + Shamir key custody) ---\n"
    "from app.privacy_gateway.router import router as private_analysis_router\n"
    "app.include_router(private_analysis_router)\n"
)


def main() -> int:
    if not PATH.exists():
        print(f"SKIP  {PATH} not found")
        return 1
    text = PATH.read_text(encoding="utf-8")
    if "private_analysis_router" in text:
        print("OK    main.py already registers the private analysis router")
        return 0
    m = re.search(r"^if __name__\s*==", text, re.M)
    new = text[: m.start()] + BLOCK.lstrip("\n") + "\n" + text[m.start():] if m else text.rstrip("\n") + "\n" + BLOCK
    shutil.copy2(PATH, PATH.with_suffix(".py.bak2"))
    PATH.write_text(new, encoding="utf-8")
    print("PATCH main.py -> /api/v1/private/* registered")
    return 0


if __name__ == "__main__":
    sys.exit(main())
