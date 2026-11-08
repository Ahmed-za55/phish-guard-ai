"""Regression tests for the two cache bugs fixed by scripts/patch_vector_cache.py."""
import os
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

pytest.importorskip("app.storage.vector_cache")
from app.storage import vector_cache as vc  # noqa: E402

BACKEND = Path(__file__).resolve().parents[2]
CONTENT = "contact alpha@example.com or bob@example.com, phone +20 100 123 4567, call +20 100 765 4321 now"
RESULT = {"summary": "mails alpha@example.com and bob@example.com; phones +20 100 123 4567 and +20 100 765 4321"}

READER = textwrap.dedent(
    """
    import sys
    from pathlib import Path
    from app.storage import vector_cache as vc
    vc.CACHE_FILE = Path(sys.argv[1])
    got = vc.ThreatMemoryCache.get(sys.argv[2])
    print("MATCH" if got == eval(sys.argv[3]) else "MISMATCH")
    """
)


def test_cached_results_restore_identically_in_any_process(tmp_path, monkeypatch):
    """Values of equal length used to swap places depending on Python's randomized string hashing."""
    cache = tmp_path / "cache.json"
    monkeypatch.setattr(vc, "CACHE_FILE", cache)
    vc.ThreatMemoryCache.set(CONTENT, RESULT)
    for seed in ("1", "2", "3", "4", "5", "6", "7", "8"):
        env = {**os.environ, "PYTHONHASHSEED": seed, "PYTHONPATH": str(BACKEND)}
        out = subprocess.run([sys.executable, "-c", READER, str(cache), CONTENT, repr(RESULT)],
                             capture_output=True, text=True, env=env, cwd=BACKEND)
        assert out.stdout.strip() == "MATCH", f"hash seed {seed}: {out.stdout} {out.stderr[-300:]}"


def test_free_text_words_from_the_input_are_never_written_in_clear(tmp_path, monkeypatch):
    cache = tmp_path / "cache.json"
    monkeypatch.setattr(vc, "CACHE_FILE", cache)
    word = "Zorblatt-Quimby-4471"
    content = f"please ask {word} about invoice"
    result = {"names": [f"asked {word}"], f"key-{word}": "ok"}
    vc.ThreatMemoryCache.set(content, result)
    assert word not in cache.read_text(encoding="utf-8")
    assert vc.ThreatMemoryCache.get(content) == result
