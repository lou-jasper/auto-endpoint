from __future__ import annotations

import uuid
from datetime import datetime
from pydantic import BaseModel, Field


def now_local():
    return datetime.now()


class BaseDomain(BaseModel):
    """领域模型基类"""

    id: str | None = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=now_local)
    updated_at: datetime = Field(default_factory=now_local)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
        }

    def touch(self):
        """更新时间"""
        self.updated_at = now_local()

    def to_dict(self) -> dict:
        return self.model_dump()

    def to_json(self) -> str:
        return self.model_dump_json()

    @classmethod
    def from_dict(cls, data: dict) -> "BaseDomain":
        return cls(**data)

    @classmethod
    def from_json(cls, json_str: str) -> "BaseDomain":
        return cls.model_validate_json(json_str)
