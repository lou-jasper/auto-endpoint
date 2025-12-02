#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import uuid

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request

from app.api.router import api_router
from app.core.config import settings
from app.lifespan import app_lifespan
from app.middleware.exception_handler import register_exception_handlers
from app.middleware.request_id import RequestIDMiddleware
from app.utils.logging import setup_logging

setup_logging()
app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
    lifespan=app_lifespan,
    debug=False
)
app.add_middleware(RequestIDMiddleware)
logger = structlog.get_logger()

register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.get("/health", tags=["系统管理"])
async def health_check(request: Request):
    trace_id = uuid.uuid4().hex
    logger.info("healthCheck", path=request.url.path)
    return {
        "code": 200,
        "msg": "ok",
        "data": {
            "env": settings.ENV,
            "version": settings.APP_VERSION,
            "trace_id": trace_id,
            "db": "connected" if settings.DATABASE_URL else "disconnected",
            "redis": "connected" if settings.REDIS_URL else "disconnected"
        }
    }
