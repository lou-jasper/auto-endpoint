#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import asyncio
import json
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional, AsyncIterator, Any
from redis.asyncio import Redis
from redis.asyncio.client import PubSub

from app.core.config import settings

# -------- Global Client --------

_redis_client: Optional[Redis] = None


async def init_redis() -> None:
    """Initialize shared Redis client during app lifespan."""
    global _redis_client
    if _redis_client is None:
        _redis_client = Redis.from_url(
            settings.REDIS_URL,
            decode_responses=False
        )


async def close_redis() -> None:
    """Dispose Redis client on shutdown."""
    global _redis_client
    if _redis_client is None:
        return

    await _redis_client.close()
    await _redis_client.connection_pool.disconnect()
    _redis_client = None


def get_redis_client() -> Redis:
    if _redis_client is None:
        raise RuntimeError("Redis not initialized. Call init_redis() in lifespan.")
    return _redis_client


# -------- FastAPI Dependency --------

async def get_redis() -> AsyncGenerator[Redis, None]:
    yield get_redis_client()


# -------- JSON Helpers --------

async def set_json(redis: Redis, key: str, value, ex: Optional[int] = None):
    raw = json.dumps(value, ensure_ascii=False)
    await redis.set(key, raw.encode("utf-8"), ex=ex)


async def get_json(redis: Redis, key: str):
    raw = await redis.get(key)
    if raw is None:
        return None
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8")
    return json.loads(raw)


# -------- Pub/Sub --------

@asynccontextmanager
async def pubsub_stream(redis: Redis, channel: str) -> AsyncIterator[PubSub]:
    pubsub = redis.pubsub()
    await pubsub.subscribe(channel)
    try:
        yield pubsub
    finally:
        await pubsub.unsubscribe(channel)
        await pubsub.close()


async def subscribe(redis: Redis, channel: str) -> AsyncIterator[bytes]:
    async with pubsub_stream(redis, channel) as pubsub:
        while True:
            message = await pubsub.get_message(
                ignore_subscribe_messages=True,
                timeout=1.0)
            if message is None:
                await asyncio.sleep(0)
                continue
            yield message["data"]


async def publish(channel: str, message: Any) -> int:
    client = get_redis_client()

    if not isinstance(message, (str, bytes)):
        message = json.dumps(message, ensure_ascii=False)

    if isinstance(message, str):
        message = message.encode("utf-8")

    return await client.publish(channel, message)
