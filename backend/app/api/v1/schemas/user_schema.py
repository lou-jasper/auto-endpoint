#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True
