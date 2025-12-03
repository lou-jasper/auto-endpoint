from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    name: str
    email: str
    password: Optional[str] = None


class UserOut(BaseModel):
    id: int
    name: str
    email: str

    model_config = dict(from_attributes=True)
