#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
功能描述:
作者: ly
版本: 1.0.0
"""
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.db.repositories.env_repo import EnvironmentRepository, EnvironmentHeaderRepository
from app.api.dependencies.dependencies import get_db_session
from app.api.v1.schemas.env_schema import EnvironmentRead, EnvironmentCreate, EnvironmentUpdate, EnvironmentHeaderRead, \
    EnvironmentHeaderCreate, GlobalVariableRead, GlobalVariableCreate
from app.core.services.env_service import EnvironmentService, EnvironmentHeaderService

# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Environment API
作者: ly
版本: 1.0.0
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List

router = APIRouter(prefix="/environments", tags=["Environment"])


def get_environment_service(
        session: AsyncSession = Depends(get_db_session)
) -> EnvironmentService:
    repo = EnvironmentRepository(db=session)
    return EnvironmentService(repo)


# --------------------------------------------------
# Environment CRUD
# --------------------------------------------------

@router.post("/", response_model=EnvironmentRead)
async def create_environment(
        data: EnvironmentCreate,
        service: EnvironmentService = Depends(get_environment_service)
):
    return await service.create(data)


@router.get("/", response_model=List[EnvironmentRead])
async def list_environments(
        skip: int = 0,
        limit: int = 20,
        service: EnvironmentService = Depends(get_environment_service)
):
    return await service.list(skip, limit)


@router.get("/{env_id}", response_model=EnvironmentRead)
async def get_environment(
        env_id: int,
        service: EnvironmentService = Depends(get_environment_service)
):
    env = await service.get(env_id)
    if not env:
        raise HTTPException(status_code=404, detail="Environment not found")
    return env


@router.put("/{env_id}", response_model=EnvironmentRead)
async def update_environment(
        env_id: int,
        data: EnvironmentUpdate,
        service: EnvironmentService = Depends(get_environment_service)
):
    env = await service.get(env_id)
    if not env:
        raise HTTPException(status_code=404, detail="Environment not found")
    return await service.update(env, data)


@router.delete("/{env_id}", response_model=dict)
async def delete_environment(
        env_id: int,
        service: EnvironmentService = Depends(get_environment_service)
):
    ok = await service.delete(env_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Environment not found")
    return {"message": "Environment deleted successfully"}


# --------------------------------------------------
# Environment Header
# --------------------------------------------------


def get_environment_header_service(
        session: AsyncSession = Depends(get_db_session)
) -> EnvironmentHeaderService:
    repo = EnvironmentHeaderRepository(db=session)
    return EnvironmentHeaderService(repo)


@router.post("/{env_id}/headers", response_model=EnvironmentHeaderRead)
async def add_environment_header(
        env_id: int,
        data: EnvironmentHeaderCreate,
        service: EnvironmentHeaderService = Depends(get_environment_header_service)
):
    return await service.add_environment_header(env_id, data)


@router.get("/{env_id}/headers", response_model=List[EnvironmentHeaderRead])
async def list_headers(
        env_id: int,
        service: EnvironmentHeaderService = Depends(get_environment_header_service)
):
    return await service.list(env_id)


# --------------------------------------------------
# Global Variables
# --------------------------------------------------

@router.post("/variables", response_model=GlobalVariableRead)
async def create_global_variable(
        data: GlobalVariableCreate,
        service: EnvironmentService = Depends(get_environment_service)
):
    return await service.c(data)


@router.get("/variables", response_model=List[GlobalVariableRead])
async def list_global_variables(
        skip: int = 0,
        limit: int = 20,
        service: EnvironmentService = Depends(get_environment_service)
):
    return await service.list_global_variables(skip, limit)


# --------------------------------------------------
# Variable Extraction Rule
# --------------------------------------------------

@router.post("/variables/{var_id}/rule", response_model=VariableExtractionRuleRead)
async def create_extraction_rule(
        var_id: int,
        data: VariableExtractionRuleCreate,
        service: EnvironmentService = Depends(get_environment_service)
):
    return await service.add_extraction_rule(var_id, data)


@router.get("/variables/{var_id}/rule", response_model=VariableExtractionRuleRead)
async def get_extraction_rule(
        var_id: int,
        service: EnvironmentService = Depends(get_environment_service)
):
    rule = await service.get_extraction_rule(var_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Extraction rule not found")
    return rule
