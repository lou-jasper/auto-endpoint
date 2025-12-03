#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

from fastapi import APIRouter, Depends
from typing import Any

from redis.asyncio import Redis
from fastapi.responses import StreamingResponse

from app.core.cache import get_redis, subscribe, get_json, set_json
from app.core.logger import get_logger

from app.workers.tasks import send_event

router = APIRouter(prefix="/v1/redis", tags=["redis"])

logger = get_logger(__name__)


@router.post("/set")
async def set_value(key: str, value: Any, redis: Redis = Depends(get_redis)):
    """
    存储 JSON 到 Redis
    """
    await set_json(redis, key, value)
    return {"message": "OK", "key": key, "value": value}


@router.get("/get")
async def get_value(key: str, redis: Redis = Depends(get_redis)):
    """
    从 Redis 读取 JSON
    """
    data = await get_json(redis, key)
    return {"key": key, "value": data}


@router.post("/publish")
async def publish_message(
        channel: str,
        message: Any,
        redis: Redis = Depends(get_redis)

):
    count = await redis.publish(channel, json.dumps(message))
    return {"channel": channel, "receivers": count}


@router.get("/subscribe")
async def subscribe_channel(
        channel: str,
        redis: Redis = Depends(get_redis)
):
    async def event_stream():
        async for msg in subscribe(redis, channel):
            text = msg.decode("utf-8")
            logger.info(f' msg {text}')
            yield f"data: {text}\n\n"

    return StreamingResponse(event_stream(), media_type="text/plain")


@router.post("/emit")
async def emit(channel: str, message: dict):
    send_event.delay(channel, message)
    return {"status": "queued"}