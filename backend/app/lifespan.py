import asyncio

from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.cache import init_redis, close_redis
from app.core.database import init_db, close_db
from app.events.consumers.consumer import event_listener


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    # ----------- startup -----------

    await init_db()
    await init_redis()
    task = asyncio.create_task(event_listener())

    yield

    # ----------- shutdown -----------
    await close_db()
    await close_redis()
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("🛑 Redis 事件监听任务已停止")
