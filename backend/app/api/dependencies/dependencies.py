#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""依赖注入配置中心 - 统一管理所有依赖实例"""

from typing import Callable, Type, TypeVar, AsyncGenerator, Optional, Any
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

# 基础设施依赖
from app.adapters.cache.cache import async_redis
from app.adapters.db.session import DatabaseManager
from app.adapters.external.http_client import HttpClient

# 仓库 & 服务
from app.adapters.db.repositories.base_repositories import BaseRepository



# 类型变量
RepoType = TypeVar("RepoType", bound=BaseRepository)


# ---------------------------------------------------------
# Redis Cache（多数情况下为单例 → 不要 yield）
# ---------------------------------------------------------
async def get_redis() -> AsyncGenerator:
    """获取全局 Redis 客户端实例。

    用于 FastAPI 依赖注入。

    Yields:
        AsyncRedis: 全局 Redis 客户端实例。
    """
    yield async_redis


# -------------------------------------------------------------------
# FastAPI 依赖注入
# -------------------------------------------------------------------
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI 依赖注入：获取数据库会话。

    Yields:
        AsyncSession: 已管理事务的数据库 Session。
    """
    manager = DatabaseManager()
    session = await manager.session()

    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


# ---------------------------------------------------------
# HTTP 客户端依赖（每请求创建、自动关闭）
# ---------------------------------------------------------
async def get_http_client(
        base_url: Optional[str] = None,
        timeout: int = 10,
        retries: int = 2
) -> AsyncGenerator[HttpClient, None]:
    async with HttpClient(
            base_url=base_url,
            timeout=timeout,
            retries=retries
    ) as client:
        yield client


# 默认客户端（固定配置）
async def get_default_http_client() -> AsyncGenerator[HttpClient, None]:
    async with HttpClient() as client:
        yield client
