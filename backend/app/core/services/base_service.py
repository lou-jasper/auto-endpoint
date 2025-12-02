#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
功能描述: 
作者: ly
版本: 1.0.0
"""

from typing import Generic, TypeVar, List, Optional, Any

ModelType = TypeVar("ModelType")
CreateType = TypeVar("CreateType")
UpdateType = TypeVar("UpdateType")


class BaseService(Generic[ModelType, CreateType, UpdateType]):
    def __init__(self, repository):
        self.repo = repository

    async def get(self, _id: Any) -> Optional[ModelType]:
        return await self.repo.get(_id)

    async def list(self, skip: int = 0, limit: int = 20) -> List[ModelType]:
        return await self.repo.list(skip, limit)

    async def create(self, obj_in: CreateType) -> ModelType:
        return await self.repo.create(obj_in)

    async def update(self, db_obj: ModelType, obj_in: UpdateType) -> ModelType:
        return await self.repo.update(db_obj, obj_in)

    async def delete(self, _id: Any) -> bool:
        return await self.repo.delete(_id)

    async def get_by_field(self, field, value) -> Optional[ModelType]:
        return await self.repo.get_by_field(field, value)
