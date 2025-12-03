#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
功能描述: 
作者: ly
版本: 1.0.0
"""

import traceback
from fastapi import Request
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.responses import JSONResponse

from app.core.logger import get_logger

logger = get_logger(__name__)


class BusinessException(Exception):

    def __init__(
            self,
            message: str,
            code: int = 40000,
            status_code: int = 400
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(message)

    def to_dict(self):
        return {
            "code": self.code,
            "message": self.message,
        }


class NotFoundException(BusinessException):
    def __init__(self, message="Resource Not Found", code=40400):
        super().__init__(message, code, status_code=404)


class UnauthorizedException(BusinessException):
    def __init__(self, message="Unauthorized", code=40100):
        super().__init__(message, code, status_code=401)


class ConflictException(BusinessException):
    def __init__(self, message="Conflict", code=40900):
        super().__init__(message, code, status_code=409)


async def business_exception_handler(request: Request, exc: BusinessException):
    logger.warning(
        "Business exception",
        method=request.method,
        path=str(request.url),
        message=exc.message,
        code=exc.code,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict()
    )


async def global_exception_handler(request: Request, exc: Exception):
    logger.error(
        "Unhandled exception",
        path=str(request.url),
        method=request.method,
        error=str(exc),
        traceback=traceback.format_exc()
    )

    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "message": "Internal Server Error",
            "detail": str(exc),
        },
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(
        "Validation error",
        path=str(request.url),
        method=request.method,
        errors=exc.errors(),
    )

    return JSONResponse(
        status_code=422,
        content={
            "code": 422,
            "message": "Validation Error",
            "detail": exc.errors(),
        },
    )


async def response_validation_exception_handler(request: Request, exc: ResponseValidationError):
    logger.error(
        "Response validation error",
        method=request.method,
        path=str(request.url),
        errors=exc.errors(),
        exc_info=True,
    )
    return JSONResponse(
        status_code=500,
        content={
            "code": 50001,
            "message": "Response Validation Error",
            "detail": exc.errors(),
        },
    )