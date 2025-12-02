#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
功能描述:
作者: ly
版本: 1.0.0
"""

from typing import Optional, List
from sqlmodel import Field, Relationship

from app.adapters.db.models.base_model import BaseModel


class Environment(BaseModel, table=True):
    __tablename__ = "environment"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, description="环境名称，如 DEV/SIT/UAT")
    base_url: str = Field(max_length=500, description="环境基础URL")
    description: Optional[str] = Field(default=None, max_length=500)

    headers: List["EnvironmentHeader"] = Relationship(back_populates="environment")


class EnvironmentHeader(BaseModel, table=True):
    __tablename__ = "environment_header"

    id: Optional[int] = Field(default=None, primary_key=True)
    header_key: str = Field(max_length=200, description="Header key")
    header_value: str = Field(max_length=500, description="Header value")
    description: Optional[str] = Field(default=None, max_length=500)

    environment_id: int = Field(foreign_key="environment.id")
    environment: Optional[Environment] = Relationship(back_populates="headers")


class GlobalVariable(BaseModel, table=True):
    __tablename__ = "global_variable"

    id: Optional[int] = Field(default=None, primary_key=True)
    variable_name: str = Field(max_length=100, description="变量名，例如 token")
    variable_value: Optional[str] = Field(default=None, max_length=500, description="变量值，可动态更新")
    description: Optional[str] = Field(default=None, max_length=500)
    is_dynamic: bool = Field(default=False, description="是否为动态变量")

    extraction_rule: Optional["VariableExtractionRule"] = Relationship(back_populates="variable")


class VariableExtractionRule(BaseModel, table=True):
    __tablename__ = "variable_extraction_rule"

    id: Optional[int] = Field(default=None, primary_key=True)
    source: str = Field(max_length=200, description="来源，如接口路径 /api/login")
    extract_method: str = Field(max_length=50, description="提取方式 jsonpath / regex / xpath")
    extract_expression: str = Field(max_length=500, description="提取表达式，例如 $.data.token")
    test_data: Optional[str] = Field(default=None, description="用于测试的返回样例数据")

    variable_id: int = Field(foreign_key="global_variable.id")
    variable: Optional[GlobalVariable] = Relationship(back_populates="extraction_rule")
