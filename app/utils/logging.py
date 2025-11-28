# app/utils/logging.py
import time, uuid, structlog
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = structlog.get_logger()

class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        rid = request.headers.get("x-request-id", str(uuid.uuid4()))
        start = time.time()
        response = await call_next(request)
        latency_ms = int((time.time() - start) * 1000)
        logger.info("req", path=request.url.path, method=request.method,
                    status=response.status_code, latency_ms=latency_ms, request_id=rid)
        response.headers["x-request-id"] = rid
        return response
