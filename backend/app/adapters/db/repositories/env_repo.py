#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
功能描述: 
作者: ly
版本: 1.0.0
"""
from typing import Any, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.db.models.env_model import (
    Environment,
    EnvironmentHeader,
    VariableExtractionRule,
    GlobalVariable
)
from app.adapters.db.repositories.base_repo import BaseRepository
from app.api.v1.schemas.env_schema import (
    EnvironmentCreate,
    EnvironmentHeaderCreate,
    VariableExtractionRuleCreate,
    GlobalVariableCreate
)


class EnvironmentRepository(BaseRepository[Environment, EnvironmentCreate]):
    def __init__(self, db: AsyncSession):
        super().__init__(Environment, db)


class EnvironmentHeaderRepository(BaseRepository[EnvironmentHeader, EnvironmentHeaderCreate]):
    def __init__(self, db: AsyncSession):
        super().__init__(EnvironmentHeader, db)


class VariableExtractionRuleRepository(BaseRepository[VariableExtractionRule, VariableExtractionRuleCreate]):
    def __init__(self, db: AsyncSession):
        super().__init__(VariableExtractionRule, db)


class GlobalVariableRepository(BaseRepository[GlobalVariable, GlobalVariableCreate]):
    def __init__(self, db: AsyncSession):
        super().__init__(GlobalVariable, db)
