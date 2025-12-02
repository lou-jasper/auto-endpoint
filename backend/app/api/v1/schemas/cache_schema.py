#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import Optional, Any


class CacheSetRequest(BaseModel):
    key: str
    value: Any
    expire_seconds: Optional[int] = None


class CacheGetRequest(BaseModel):
    key: str


class CacheDeleteRequest(BaseModel):
    key: str
