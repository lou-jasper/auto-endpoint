#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

from typing import Optional

from pydantic import EmailStr
from sqlmodel import SQLModel, Field

from app.adapters.db.models.base_model import BaseModel


class UserModel(BaseModel, table=True):
    """用户数据库模型（ORM）

    说明：
        - 继承 BaseModel，拥有 created_at / updated_at。
        - 使用 SQLModel 定义数据库字段。
        - table=True 表示这是一个真实表。
    """

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)

    username: str = Field(
        index=True,
        nullable=False,
        description="用户名"
    )

    email: EmailStr = Field(
        index=True,
        nullable=False,
        unique=True,
        description="邮箱地址"
    )

    password_hash: str = Field(
        nullable=False,
        description="哈希后的密码"
    )

    is_active: bool = Field(
        default=True,
        nullable=False,
        description="是否启用"
    )

    is_superuser: bool = Field(
        default=False,
        nullable=False,
        description="是否管理员"
    )
