"""Per-IP token-bucket-ish rate limiter (simple sliding window).

Not horizontally scalable; fine for a single-process portfolio demo.
"""

from __future__ import annotations

import time
from collections import deque
from threading import Lock


class RateLimiter:
    def __init__(self, per_minute: int) -> None:
        self._per_minute = max(1, per_minute)
        self._window = 60.0
        self._buckets: dict[str, deque[float]] = {}
        self._lock = Lock()

    def allow(self, key: str) -> bool:
        now = time.time()
        cutoff = now - self._window
        with self._lock:
            bucket = self._buckets.setdefault(key, deque())
            while bucket and bucket[0] < cutoff:
                bucket.popleft()
            if len(bucket) >= self._per_minute:
                return False
            bucket.append(now)
            return True


_limiter: RateLimiter | None = None


def get_limiter() -> RateLimiter:
    global _limiter
    if _limiter is None:
        from .settings import get_settings

        _limiter = RateLimiter(get_settings().rate_limit_per_minute)
    return _limiter
