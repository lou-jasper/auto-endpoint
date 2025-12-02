#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
功能描述: 
作者: ly
版本: 1.0.0
"""
from __future__ import annotations

from pydantic import Field, EmailStr

from app.core.domain.base_domain import BaseDomain


class UserDomain(BaseDomain):
    name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
