#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
功能描述: 
作者: ly
版本: 1.0.0
"""

from fastapi import APIRouter
from app.adapters.cache.cache import async_redis
from app.api.v1.schemas.cache_schema import CacheSetRequest, CacheGetRequest, CacheDeleteRequest

router = APIRouter(prefix="/cache", tags=["Cache"])


@router.post("/set")
async def cache_set(body: CacheSetRequest):
    ok = await async_redis.set(body.key, body.value, body.expire_seconds)
    return {
        "success": ok,
        "key": body.key,
        "value": body.value,
        "expire": body.expire_seconds
    }


@router.post("/get")
async def cache_get(body: CacheGetRequest):
    value = await async_redis.get(body.key)
    return {
        "key": body.key,
        "value": value
    }


@router.post("/delete")
async def cache_delete(body: CacheDeleteRequest):
    ok = await async_redis.delete(body.key)
    return {
        "success": ok,
        "key": body.key
    }
