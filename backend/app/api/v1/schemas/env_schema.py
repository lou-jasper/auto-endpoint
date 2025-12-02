#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
功能描述: 
作者: ly
版本: 1.0.0
"""
from typing import Optional

from sqlmodel import SQLModel


class EnvironmentRead(SQLModel):
    id: int
    name: str
    base_url: str
    description: Optional[str]


class EnvironmentCreate(SQLModel):
    name: str
    base_url: str
    description: Optional[str] = None


class EnvironmentUpdate(SQLModel):
    name: Optional[str] = None
    base_url: Optional[str] = None
    description: Optional[str] = None


class EnvironmentHeaderRead(SQLModel):
    id: int
    header_key: str
    header_value: str
    description: Optional[str]
    environment_id: int


class EnvironmentHeaderCreate(SQLModel):
    header_key: str
    header_value: str
    description: Optional[str] = None
    environment_id: int


class EnvironmentHeaderUpdate(SQLModel):
    header_key: Optional[str] = None
    header_value: Optional[str] = None
    description: Optional[str] = None
    environment_id: Optional[int] = None


class GlobalVariableRead(SQLModel):
    id: int
    variable_name: str
    variable_value: Optional[str]
    description: Optional[str]
    is_dynamic: bool


class GlobalVariableCreate(SQLModel):
    variable_name: str
    variable_value: Optional[str] = None
    description: Optional[str] = None
    is_dynamic: bool = False


class GlobalVariableUpdate(SQLModel):
    variable_name: Optional[str] = None
    variable_value: Optional[str] = None
    description: Optional[str] = None
    is_dynamic: Optional[bool] = None


class VariableExtractionRuleRead(SQLModel):
    id: int
    source: str
    extract_method: str
    extract_expression: str
    test_data: Optional[str]
    variable_id: int


class VariableExtractionRuleCreate(SQLModel):
    source: str
    extract_method: str
    extract_expression: str
    test_data: Optional[str] = None
    variable_id: int


class VariableExtractionRuleUpdate(SQLModel):
    source: Optional[str] = None
    extract_method: Optional[str] = None
    extract_expression: Optional[str] = None
    test_data: Optional[str] = None
    variable_id: Optional[int] = None
