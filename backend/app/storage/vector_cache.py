import json
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional

CACHE_FILE = Path(__file__).resolve().parent.parent / "storage" / "threat_cache.json"
CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)

class ThreatMemoryCache:
    """
    Local Vector & Threat Intelligence Cache: Stores cryptographic fingerprints 
    of analyzed payloads and mathematical metrics for lightning-fast matching.
    """
    @staticmethod
    def _hash_payload(content: str) -> str:
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    @classmethod
    def get(cls, content: str) -> Optional[Dict[str, Any]]:
        if not CACHE_FILE.exists():
            return None
        try:
            data = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
            key = cls._hash_payload(content)
            return data.get(key)
        except Exception:
            return None

    @classmethod
    def set(cls, content: str, analysis_result: Dict[str, Any]) -> None:
        try:
            data = {}
            if CACHE_FILE.exists():
                data = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
            key = cls._hash_payload(content)
            data[key] = analysis_result
            CACHE_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
        except Exception:
            pass