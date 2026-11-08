import json
import hashlib
import re
from pathlib import Path
from typing import Dict, Any, Optional
from urllib.parse import urlsplit

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

    _PRIVACY_SCHEMA = 4
    _WORD_PATTERN = re.compile(r"[^\W_](?:[\w\-]{2,})[^\W_]", re.UNICODE)  # words of 4+ characters
    _URL_PATTERN = re.compile(r"https?://[^\s<>\"']+", re.IGNORECASE)
    _EMAIL_PATTERN = re.compile(
        r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+"
    )
    _LONG_NUMBER_PATTERN = re.compile(r"(?<!\w)\+?\d[\d(). -]{5,}\d(?!\w)")
    _CREDENTIAL_PATTERN = re.compile(
        r"(?i)\b(?:password|passwd|passcode|token|api[_-]?key|secret|authorization)"
        r"\s*[:=]\s*[^\s&;,]+"
    )

    @classmethod
    def _sensitive_values(cls, content: str) -> list[str]:
        """Return request-derived strings that must not be serialized in cache values."""
        values = {content} if content else set()
        values.update(
            match.group(0).rstrip(".,!?;:)]}'\"")
            for match in cls._URL_PATTERN.finditer(content)
        )
        values.update(match.group(0) for match in cls._EMAIL_PATTERN.finditer(content))
        values.update(match.group(0) for match in cls._LONG_NUMBER_PATTERN.finditer(content))
        values.update(match.group(0) for match in cls._CREDENTIAL_PATTERN.finditer(content))
        # Free text (names, reference codes) is not matched by the patterns above, so keep every word.
        words = sorted(set(cls._WORD_PATTERN.findall(content)), key=lambda w: (-len(w), w))[:500]
        values.update(words)

        # Hostnames can also appear separately in detailed analysis output.
        for value in tuple(values):
            if value.startswith(("http://", "https://")):
                try:
                    hostname = urlsplit(value).hostname
                except ValueError:
                    hostname = None
                if hostname:
                    values.add(hostname)

        # Sort by (length, text): the cache stores INDEXES into this list, so the order must never vary.
        return sorted((value for value in values if value), key=lambda v: (-len(v), v))

    @classmethod
    def _sanitize_string(cls, value: str, sensitive_values: list[str]) -> list[Any]:
        """Encode a string as literal text and typed references to current input."""
        segments = []
        cursor = 0
        while cursor < len(value):
            match_at = len(value)
            match_value = None
            for sensitive_value in sensitive_values:
                position = value.find(sensitive_value, cursor)
                if position >= 0 and (position < match_at or (
                    position == match_at and match_value is not None
                    and len(sensitive_value) > len(match_value)
                )):
                    match_at, match_value = position, sensitive_value
            if match_value is None:
                segments.append([0, value[cursor:]])
                break
            if match_at > cursor:
                segments.append([0, value[cursor:match_at]])
            segments.append([1, sensitive_values.index(match_value)])
            cursor = match_at + len(match_value)
        if not value:
            segments.append([0, ""])
        return segments

    @classmethod
    def _sanitize_result(cls, value: Any, sensitive_values: list[str]) -> Any:
        """Encode every node, so user data cannot impersonate restoration markers."""
        if isinstance(value, dict):
            pairs = []
            for key, item in value.items():
                if not isinstance(key, str):
                    raise TypeError("Cache result dictionary keys must be strings")
                normalized_key = key.lower()
                if normalized_key == "analysis_commentary":
                    item = ""
                elif normalized_key == "sanitized_text":
                    item = None
                elif normalized_key == "decoded_hidden_artifacts":
                    item = []
                elif normalized_key == "apocalypse_tier_v2_0":
                    continue
                pairs.append([
                    cls._sanitize_result(key, sensitive_values),
                    cls._sanitize_result(item, sensitive_values),
                ])
            return ["d", pairs]
        if isinstance(value, (list, tuple)):
            return ["l", [cls._sanitize_result(item, sensitive_values) for item in value]]
        if isinstance(value, str):
            return ["s", cls._sanitize_string(value, sensitive_values)]
        return ["v", value]

    @classmethod
    def _restore_result(cls, value: Any, content: str, sensitive_values: list[str]) -> Any:
        """Decode typed nodes and restore only validated, scoped input references."""
        if not isinstance(value, list) or len(value) != 2:
            raise ValueError("Invalid privacy cache node")
        kind, payload = value
        if kind == "d" and isinstance(payload, list):
            result = {}
            for pair in payload:
                if not isinstance(pair, list) or len(pair) != 2:
                    raise ValueError("Invalid privacy cache mapping")
                key = cls._restore_result(pair[0], content, sensitive_values)
                if not isinstance(key, str) or key in result:
                    raise ValueError("Invalid or duplicate privacy cache key")
                result[key] = cls._restore_result(pair[1], content, sensitive_values)
            return result
        if kind == "l" and isinstance(payload, list):
            return [cls._restore_result(item, content, sensitive_values) for item in payload]
        if kind == "s" and isinstance(payload, list):
            output = []
            for segment in payload:
                if not isinstance(segment, list) or len(segment) != 2:
                    raise ValueError("Invalid privacy cache string segment")
                segment_kind, segment_value = segment
                if segment_kind == 0 and isinstance(segment_value, str):
                    output.append(segment_value)
                elif (segment_kind == 1 and isinstance(segment_value, int)
                      and 0 <= segment_value < len(sensitive_values)):
                    output.append(sensitive_values[segment_value])
                else:
                    raise ValueError("Invalid privacy cache string reference")
            return "".join(output)
        if kind == "v" and (
            payload is None or isinstance(payload, (str, int, float, bool))
        ):
            return payload
        raise ValueError("Invalid privacy cache node type")

    @classmethod
    def get(cls, content: str) -> Optional[Dict[str, Any]]:
        if not CACHE_FILE.exists():
            return None
        try:
            data = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
            key = cls._hash_payload(content)
            entry = data.get(key)
            # Legacy entries predate cache sanitization. Treat them as misses rather
            # than returning a value that may contain persisted input or URLs.
            if (
                not isinstance(entry, dict)
                or entry.get("_cache_privacy_schema") != cls._PRIVACY_SCHEMA
            ):
                return None
            result = entry.get("result")
            if not isinstance(result, list):
                return None
            restored = cls._restore_result(result, content, cls._sensitive_values(content))
            return restored if isinstance(restored, dict) else None
        except Exception:
            return None

    @classmethod
    def set(cls, content: str, analysis_result: Dict[str, Any]) -> None:
        try:
            data = {}
            if CACHE_FILE.exists():
                data = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
            key = cls._hash_payload(content)
            data[key] = {
                "_cache_privacy_schema": cls._PRIVACY_SCHEMA,
                "result": cls._sanitize_result(
                    analysis_result, cls._sensitive_values(content)
                ),
            }
            CACHE_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
        except Exception:
            pass
