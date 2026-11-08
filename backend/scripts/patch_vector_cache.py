"""Two fixes for backend/app/storage/vector_cache.py (safe to run twice, keeps a .bak copy).

1. Deterministic ordering. Cached strings point at entries of the `sensitive_values` list by INDEX.
   That list was sorted by length only, so equal-length values (two phone numbers, two emails) came back
   in a different order in each Python process (string hashing is randomized) and the cache could return
   the WRONG value. It is now sorted by (length, text).
2. Words from the input are sensitive too. Free text such as names or reference codes is not caught by the
   patterns, so a result string or dictionary key that contained such a word was written to disk in clear.
   Every word of 4+ characters in the input is now stored as a reference. Old entries (schema 3) are ignored.

Run:  python backend/scripts/patch_vector_cache.py
"""
import re
import shutil
import sys
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "app" / "storage" / "vector_cache.py"


def main() -> int:
    if not PATH.exists():
        print(f"SKIP  {PATH} not found")
        return 1
    text = PATH.read_text(encoding="utf-8")
    if "_WORD_PATTERN" in text:
        print("OK    vector_cache.py already patched")
        return 0

    schema_line = (
        "_PRIVACY_SCHEMA = 4\n"
        '    _WORD_PATTERN = re.compile(r"[^\\W_](?:[\\w\\-]{2,})[^\\W_]", re.UNICODE)  # words of 4+ characters'
    )
    words_block = (
        "        # Free text (names, reference codes) is not matched by the patterns above, so keep every word.\n"
        "        words = sorted(set(cls._WORD_PATTERN.findall(content)), key=lambda w: (-len(w), w))[:500]\n"
        "        values.update(words)\n"
    )
    sort_line = (
        "# Sort by (length, text): the cache stores INDEXES into this list, so the order must never vary.\n"
        "        return sorted((value for value in values if value), key=lambda v: (-len(v), v))"
    )
    # lambdas: the replacement texts contain backslashes that re.sub would otherwise treat as escapes
    new, n1 = re.subn(r"_PRIVACY_SCHEMA\s*=\s*3\b", lambda m: schema_line, text, count=1)
    new, n2 = re.subn(
        r"(values\.update\(match\.group\(0\) for match in cls\._CREDENTIAL_PATTERN\.finditer\(content\)\)\n)",
        lambda m: m.group(1) + words_block, new, count=1)
    new, n3 = re.subn(
        r"return sorted\(\(value for\s*value in values if value\),\s*key=len,\s*reverse=True\)",
        lambda m: sort_line, new, count=1)
    if not (n1 and n2 and n3):
        print(f"WARN  unexpected file shape (schema:{n1} words:{n2} sort:{n3}) - not modified")
        return 1
    shutil.copy2(PATH, PATH.with_suffix(".py.bak"))
    PATH.write_text(new, encoding="utf-8")
    print("PATCH vector_cache.py -> deterministic order, input words stored as references, schema 4")
    return 0


if __name__ == "__main__":
    sys.exit(main())
