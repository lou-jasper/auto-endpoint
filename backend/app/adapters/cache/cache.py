#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
import asyncio
from typing import Any, Optional

import redis.asyncio as redis
from redis.exceptions import ConnectionError, TimeoutError
from app.core.config import settings

logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, settings.LOG_LEVEL))


class AsyncRedis:
    _instance: Optional["AsyncRedis"] = None
    _lock = asyncio.Lock()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._redis_client: Optional[redis.Redis] = None
        self._init_client()

    def _init_client(self) -> None:
        if not settings.REDIS_URL:
            raise ValueError("REDIS_URL 未配置，请在配置文件中提供。")

        try:
            self._redis_client = redis.from_url(
                settings.REDIS_URL,
                decode_responses=True,
                socket_timeout=5,
                socket_connect_timeout=5,
                health_check_interval=30,
                max_connections=20,
                retry_on_timeout=True,
            )
            logger.info("Redis 客户端初始化成功")
        except Exception as exc:
            logger.error(f"Redis 初始化失败: {exc}", exc_info=True)
            raise

    @property
    def client(self) -> redis.Redis:
        if not self._redis_client or not self._redis_client.connection_pool:
            self._init_client()
        return self._redis_client

    async def get(self, key: str) -> Optional[Any]:
        try:
            value = await self.client.get(key)
            if value is None:
                return None
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        except (ConnectionError, TimeoutError):
            logger.warning(f"Redis GET 连接异常：{key}")
            self._init_client()
            return None

    async def set(self, key: str, value: Any, expire_seconds: Optional[int] = None) -> bool:
        try:
            data = json.dumps(value, ensure_ascii=False)
            if expire_seconds:
                return await self.client.setex(key, expire_seconds, data)
            return await self.client.set(key, data)
        except Exception as exc:
            logger.error(f"Redis SET 失败：{key} -> {exc}")
            return False

    async def delete(self, key: str) -> bool:
        try:
            return await self.client.delete(key) > 0
        except Exception as exc:
            logger.error(f"Redis DEL 失败：{key} -> {exc}")
            return False

    async def exists(self, key: str) -> bool:
        return await self.client.exists(key) == 1

    async def expire(self, key: str, seconds: int) -> bool:
        return seconds > 0 and await self.client.expire(key, seconds) == 1

    async def clear_pattern(self, pattern: str, batch_size: int = 100) -> int:
        try:
            cursor, total_deleted = 0, 0
            while True:
                cursor, keys = await self.client.scan(
                    cursor=cursor, match=pattern, count=batch_size
                )
                if keys:
                    total_deleted += await self.client.delete(*keys)
                if cursor == 0:
                    break
            return total_deleted
        except Exception as exc:
            logger.error(f"批量清理失败：{pattern} -> {exc}")
            return 0


async_redis = AsyncRedis()
