import time
from collections import defaultdict, deque
from threading import Lock
from fastapi import Request


class RateLimiter:
    def __init__(
        self,
        max_requests: int = 10,
        window_seconds: int = 60,
    ):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests: dict[str, deque[float]] = defaultdict(deque)
        self._lock = Lock()

    def get_client_key(self, request: Request) -> str:
        # Check standard headers
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            ip = forwarded.split(",")[0].strip()
        elif request.client and request.client.host:
            ip = request.client.host
        else:
            ip = "127.0.0.1"

        # Normalize localhost IPv6 to IPv4 so both count against the same quota
        if ip in ("::1", "localhost"):
            ip = "127.0.0.1"

        return ip

    def allow(self, request: Request) -> tuple[bool, int]:
        now = time.time()
        key = self.get_client_key(request)

        with self._lock:
            bucket = self._requests[key]
            cutoff = now - self.window_seconds

            # Remove expired requests
            while bucket and bucket[0] <= cutoff:
                bucket.popleft()

            # Check limit
            if len(bucket) >= self.max_requests:
                retry_after = max(
                    1,
                    int(self.window_seconds - (now - bucket[0])),
                )
                return False, retry_after

            # Record this request
            bucket.append(now)
            return True, 0