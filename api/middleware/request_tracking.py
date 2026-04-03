"""Request tracking middleware for analytics"""

import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


class RequestTrackingMiddleware(BaseHTTPMiddleware):
    """Tracks every request: timing, path, and status code"""

    def __init__(self, app, stats_service=None):
        super().__init__(app)
        self.stats_service = stats_service

    async def dispatch(self, request: Request, call_next) -> Response:
        start = time.time()
        path = request.url.path

        response = await call_next(request)

        duration = time.time() - start

        if self.stats_service:
            self.stats_service.record_request(path)

        if duration > 1.0:
            logger.warning(f"Slow request: {request.method} {path} took {duration:.2f}s")

        response.headers["X-Response-Time"] = f"{duration:.4f}s"
        response.headers["X-API-Version"] = "1.0.0"

        return response
