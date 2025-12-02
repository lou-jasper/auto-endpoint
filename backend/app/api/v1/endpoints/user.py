#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
功能描述: 
作者: ly
版本: 1.0.0
"""

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.dependencies import get_db_session
from app.api.v1.schemas.user_schema import UserOut, UserCreate, UserUpdate
from app.core.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserOut)
async def create_user(
        data: UserCreate,
        db: AsyncSession = Depends(get_db_session)
):
    user = await UserService.create_user(db, data)
    return user


@router.get("/{user_id}", response_model=UserOut)
async def get_user(
        user_id: str,
        db: AsyncSession = Depends(get_db_session)
):
    user = await UserService.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserOut)
async def update_user(
        user_id: str,
        data: UserUpdate,
        db: AsyncSession = Depends(get_db_session)
):
    user = await UserService.update_user(db, user_id, data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}")
async def delete_user(
        user_id: str,
        db: AsyncSession = Depends(get_db_session)
):
    ok = await UserService.delete_user(db, user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
    return {"success": True}
