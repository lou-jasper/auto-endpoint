#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
功能描述: 
作者: ly
版本: 1.0.0
"""

from app.adapters.db.models.env_model import (
    Environment,
    EnvironmentHeader,
    GlobalVariable,
    VariableExtractionRule
)
from app.adapters.db.repositories.env_repo import EnvironmentRepository, EnvironmentHeaderRepository, \
    GlobalVariableRepository, VariableExtractionRuleRepository
from app.api.v1.schemas.env_schema import (
    EnvironmentCreate,
    EnvironmentUpdate,
    EnvironmentHeaderCreate,
    EnvironmentHeaderUpdate,
    GlobalVariableCreate,
    GlobalVariableUpdate,
    VariableExtractionRuleCreate,
    VariableExtractionRuleUpdate
)
from app.core.services.base_service import BaseService


class EnvironmentService(
    BaseService[Environment, EnvironmentCreate, EnvironmentUpdate]
):
    def __init__(self, repo: EnvironmentRepository):
        super().__init__(repo)
        self.repo = repo

    async def create_global_variable(self, data):
        pass

    async def list_global_variables(self, skip, limit):
        pass


class EnvironmentHeaderService(
    BaseService[EnvironmentHeader, EnvironmentHeaderCreate, EnvironmentHeaderUpdate]
):
    def __init__(self, repo: EnvironmentHeaderRepository):
        super().__init__(repo)
        self.repo = repo

    async def add_environment_header(self, env_id, data):
        pass

    async def list_headers(self, env_id):
        pass


class GlobalVariableService(
    BaseService[GlobalVariable, GlobalVariableCreate, GlobalVariableUpdate]
):
    def __init__(self, repo: GlobalVariableRepository):
        super().__init__(repo)
        self.repo = repo


class VariableExtractionRuleService(
    BaseService[VariableExtractionRule, VariableExtractionRuleCreate, VariableExtractionRuleUpdate]
):
    def __init__(self, repo: VariableExtractionRuleRepository):
        super().__init__(repo)
        self.repo = repo

    async def create_rule(self, var_id, data):
        pass

    async def get_rule(self, var_id):
        pass
