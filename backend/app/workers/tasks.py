#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
功能描述: 
作者: ly
版本: 1.0.0
"""

import json
import asyncio
from redis.asyncio import Redis
from app.core.celery_app import celery_app


async def _async_publish(channel: str, message: dict):
    redis = Redis(host="localhost", port=6379, db=0)
    await redis.publish(channel, json.dumps(message, ensure_ascii=False))
    await redis.close()


@celery_app.task(name="app.workers.tasks.send_event")
def send_event(channel: str, data: dict):
    asyncio.run(_async_publish(channel, data))
