#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from contextlib import asynccontextmanager
from fastapi import FastAPI

from redis.exceptions import ConnectionError as RedisConnectionError, TimeoutError as RedisTimeoutError, RedisError
from sqlalchemy.exc import SQLAlchemyError

from app.adapters.cache.cache import async_redis
from app.adapters.db.session import init_db, close_db


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    try:
        client = async_redis.client
        await client.ping()
        await init_db()
    except (RedisConnectionError, RedisTimeoutError, RedisError):
        raise

    yield

    try:
        client = async_redis.client
        if client:
            await client.close()
            await client.connection_pool.disconnect()
    except (RedisConnectionError, RedisTimeoutError, RedisError):
        pass

    try:
        await close_db()
    except SQLAlchemyError:
        pass
