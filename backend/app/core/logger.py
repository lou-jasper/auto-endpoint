import logging
import uuid
from json import JSONDecodeError

import structlog

import json
from fastapi import Request

from starlette.types import ASGIApp, Scope, Receive, Send


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
    )

    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.dev.ConsoleRenderer(),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    )


def get_logger(name=None):
    return structlog.get_logger(name)


async def request_id_middleware(request: Request, call_next):
    structlog.contextvars.clear_contextvars()

    rid = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    structlog.contextvars.bind_contextvars(reqid=rid)

    response = await call_next(request)
    response.headers["X-Request-ID"] = rid
    return response


logger = get_logger(__name__)

import json
from json import JSONDecodeError
from starlette.types import ASGIApp, Scope, Receive, Send
from app.core.logger import logger


class BestLogMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        # ---- 捕获 request body ----
        body_chunks = []

        async def receive_wrapper():
            message = await receive()
            if message["type"] == "http.request":
                body_chunks.append(message.get("body", b""))
            return message

        # 先执行下游，避免错过 body 事件
        resp_body = b""

        async def send_wrapper(message):
            nonlocal resp_body
            if message["type"] == "http.response.body":
                resp_body += message.get("body", b"")
            await send(message)

        await self.app(scope, receive_wrapper, send_wrapper)

        # ---- request body ----
        req_bytes = b"".join(body_chunks)
        req_str = req_bytes.decode() if req_bytes else ""

        try:
            req_json = json.loads(req_str)
        except JSONDecodeError:
            req_json = req_str or None

        # ---- response body ----
        resp_str = resp_body.decode() if resp_body else ""
        try:
            resp_json = json.loads(resp_str)
        except JSONDecodeError:
            resp_json = resp_str or None

        # ---- structlog 输出 ----
        logger.info(
            "HTTP request",
            method=scope["method"],
            path=scope["path"],
            body=req_json
        )

        logger.info(
            "HTTP response",
            path=scope["path"],
            body=resp_json
        )

        return None
