import uuid
import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request_id = str(uuid.uuid4())
        trace_id = uuid.uuid4().hex

        logger = structlog.get_logger()
        logger = logger.bind(request_id=request_id, trace_id=trace_id)

        response: Response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Trace-ID"] = trace_id

        logger.info("response.sent", path=request.url.path, method=request.method)

        return response
