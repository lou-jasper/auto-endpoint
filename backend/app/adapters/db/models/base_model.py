from datetime import datetime, timezone
from typing import Optional, Any

from sqlalchemy import Column, DateTime, func, inspect
from sqlmodel import SQLModel, Field


class BaseModel(SQLModel):
    __abstract__ = True

    created_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

    updated_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime(timezone=True),
            onupdate=func.now(),
            nullable=True,
        )
    )

    def update(self, **kwargs: Any) -> None:
        mapper = inspect(self.__class__)
        column_keys = {c.key for c in mapper.columns}

        for key, value in kwargs.items():
            if key in column_keys and key not in {"id", "created_at"}:
                setattr(self, key, value)

        self.updated_at = datetime.now(timezone.utc)
