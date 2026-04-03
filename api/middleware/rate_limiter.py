"""Simple in-memory rate limiter"""

import time
import threading
from typing import Dict, Tuple
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse


class RateLimiter(BaseHTTPMiddleware):
    """Token-bucket rate limiter per IP address"""

    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.rpm = requests_per_minute
        self._buckets: Dict[str, Tuple[float, int]] = {}
        self._lock = threading.Lock()

    def _get_client_ip(self, request: Request) -> str:
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host if request.client else "unknown"

    def _check_rate(self, ip: str) -> Tuple[bool, int]:
        now = time.time()
        with self._lock:
            if ip in self._buckets:
                window_start, count = self._buckets[ip]
                if now - window_start > 60:
                    self._buckets[ip] = (now, 1)
                    return True, self.rpm - 1
                elif count >= self.rpm:
                    remaining = 0
                    return False, remaining
                else:
                    self._buckets[ip] = (window_start, count + 1)
                    return True, self.rpm - count - 1
            else:
                self._buckets[ip] = (now, 1)
                return True, self.rpm - 1

    async def dispatch(self, request: Request, call_next):
        if request.url.path in ("/health", "/", "/favicon.png", "/favicon.ico"):
            return await call_next(request)

        ip = self._get_client_ip(request)
        allowed, remaining = self._check_rate(ip)

        if not allowed:
            return JSONResponse(
                status_code=429,
                content={
                    "success": False,
                    "error": "Rate limit exceeded",
                    "detail": f"Maximum {self.rpm} requests per minute. Please wait.",
                },
                headers={
                    "X-RateLimit-Limit": str(self.rpm),
                    "X-RateLimit-Remaining": "0",
                    "Retry-After": "60",
                },
            )

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self.rpm)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        return response
