#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""异常处理器（统一注册）"""

import traceback
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from loguru import logger

from app.core.exceptions import (
    UserNotFoundError,
    UserAlreadyExistsError,
    InvalidUserUpdateError
)


# ========== 工具函数：构建更漂亮/更可解析的异常日志 ==========
def build_error_log(exc: Exception):
    """生成结构化异常日志（主异常 + cause/context 链）"""

    error_blocks = []

    # 主异常
    main_tb = traceback.format_exc()
    error_blocks.append({
        "type": type(exc).__name__,
        "message": str(exc),
        "stack": main_tb,
        "chain_type": "main",
    })

    # 显式异常链（raise ... from ...）
    chain_exc = exc
    while chain_exc.__cause__:
        chain_exc = chain_exc.__cause__
        tb = ''.join(traceback.format_tb(chain_exc.__traceback__)) if chain_exc.__traceback__ else ""

        error_blocks.append({
            "type": type(chain_exc).__name__,
            "message": str(chain_exc),
            "stack": tb,
            "chain_type": "cause",
        })

    # 隐式异常链（异常嵌套）
    chain_exc = exc
    while chain_exc.__context__ and chain_exc.__context__ is not exc:
        chain_exc = chain_exc.__context__
        tb = ''.join(traceback.format_tb(chain_exc.__traceback__)) if chain_exc.__traceback__ else ""

        error_blocks.append({
            "type": type(chain_exc).__name__,
            "message": str(chain_exc),
            "stack": tb,
            "chain_type": "context",
        })

    return error_blocks


# ========== 全局异常处理器（核心优化版） ==========
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理器（格式化日志、打印异常链）"""

    trace_id = getattr(request.state, "trace_id", "")

    # 构建结构化异常块
    error_blocks = build_error_log(exc)

    # ----------- 统一结构化 JSON 日志（推荐用于生产） -----------
    logger.error({
        "event": "UnhandledException",
        "trace_id": trace_id,
        "path": request.url.path,
        "method": request.method,
        "client": request.client.host if request.client else None,
        "exception_chain": error_blocks,
    })

    # ----------- 美观可读的控制台输出（开发环境可用） -----------
    print("\n" + "=" * 100)
    print("🔥 全局异常捕获（Formatted Trace）")
    print(f"Trace ID: {trace_id}")
    print(f"URL     : {request.method} {request.url.path}")
    print("-" * 100)

    for idx, block in enumerate(error_blocks):
        print(f"[{idx}] {block['chain_type'].upper()} Exception")
        print(f"类型   : {block['type']}")
        print(f"信息   : {block['message']}")
        print("堆栈   :")
        print(block["stack"])
        print("-" * 100)

    print("=" * 100 + "\n")

    # ----------- 返回标准化响应 -----------
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "message": "服务器内部错误",
            "trace_id": trace_id,
        }
    )


# ========== 用户异常（保持不变） ==========
async def user_not_found_handler(request: Request, exc: UserNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"code": 404, "message": str(exc), "trace_id": getattr(request.state, "trace_id", "")}
    )


async def user_already_exists_handler(request: Request, exc: UserAlreadyExistsError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"code": 409, "message": str(exc), "trace_id": getattr(request.state, "trace_id", "")}
    )


async def invalid_update_handler(request: Request, exc: InvalidUserUpdateError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"code": 400, "message": str(exc), "trace_id": getattr(request.state, "trace_id", "")}
    )


# ========== 注册函数 ==========
def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(UserNotFoundError, user_not_found_handler)
    app.add_exception_handler(UserAlreadyExistsError, user_already_exists_handler)
    app.add_exception_handler(InvalidUserUpdateError, invalid_update_handler)
    app.add_exception_handler(Exception, global_exception_handler)
