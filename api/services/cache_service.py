"""Simple in-memory cache with TTL support"""

import time
import threading
from typing import Any, Optional


class CacheService:
    """Thread-safe in-memory cache with TTL expiration"""

    def __init__(self, default_ttl: int = 300):
        self._cache: dict = {}
        self._lock = threading.Lock()
        self.default_ttl = default_ttl
        self.hits = 0
        self.misses = 0

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            if key in self._cache:
                value, expires_at = self._cache[key]
                if time.time() < expires_at:
                    self.hits += 1
                    return value
                del self._cache[key]
            self.misses += 1
            return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        with self._lock:
            expires_at = time.time() + (ttl or self.default_ttl)
            self._cache[key] = (value, expires_at)

    def invalidate(self, key: str):
        with self._lock:
            self._cache.pop(key, None)

    def clear(self):
        with self._lock:
            self._cache.clear()

    def cleanup(self):
        """Remove expired entries"""
        now = time.time()
        with self._lock:
            expired = [k for k, (_, exp) in self._cache.items() if now >= exp]
            for k in expired:
                del self._cache[k]

    @property
    def stats(self) -> dict:
        total = self.hits + self.misses
        return {
            "size": len(self._cache),
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": round(self.hits / total, 4) if total > 0 else 0,
        }
