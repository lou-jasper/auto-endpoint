#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
基础模型定义（BaseModel）
=======================

说明：
    - 所有 SQLModel 数据表模型的基础类。
    - 提供 created_at / updated_at 自动时间字段。
    - 提供通用 update() 方法，用于更新实例属性。
    - 配置项（时区、数据库行为等）由外部配置文件管理。

文档风格：
    - 使用中文 Google Doc Style。
"""

from datetime import datetime
from typing import Any
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func


class BaseModel(SQLModel):
    """所有数据库模型的基础类。

    说明：
        - 作为所有持久化实体的父类。
        - 自动维护创建时间与更新时间字段。
        - 提供 update() 方法用于模型属性的安全更新。

    Attributes:
        created_at (datetime): 创建时间，由数据库默认生成。
        updated_at (datetime): 更新时间，可为空，由数据库 onupdate 自动更新。
    """

    __abstract__ = True

    created_at: datetime = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        ),
    )

    updated_at: datetime = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            onupdate=func.now(),
            nullable=True,
        ),
    )

    async def update(self, **kwargs: Any) -> None:
        """更新当前模型实例的属性。

        说明：
            - 不更新 id、created_at 等只读字段。
            - 仅更新模型中实际存在的字段。
            - 赋值后立即更新 updated_at。

        Args:
            **kwargs (Any): 需要更新的模型属性及其值。

        Returns:
            None
        """
        allowed_fields = [
            name
            for name in self.model_fields.keys()
            if name not in {"id", "created_at"}
        ]

        for key, value in kwargs.items():
            if key in allowed_fields and value is not None:
                setattr(self, key, value)

        # 手动更新时间戳（数据库本身也会更新，双保险）
        self.updated_at = datetime.now()
