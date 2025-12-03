#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
功能描述:
作者: ly
版本: 1.0.0
"""
import asyncio
import json

from redis.asyncio import Redis

from app.core.logger import get_logger

logger = get_logger(__name__)


async def handle_message(msg: dict):
    logger.info(f'msg {msg}')


async def event_listener():
    redis = Redis(host="localhost", port=6379, db=0)
    pubsub = redis.pubsub()
    await pubsub.subscribe("app.workers.tasks.send_event")

    print("🎧 正在监听 Redis channel: app.workers.tasks.send_event")

    try:
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)

            if message:
                raw = message["data"]
                data = json.loads(raw)
                await handle_message(data)

            await asyncio.sleep(0.01)
    finally:
        await pubsub.close()
