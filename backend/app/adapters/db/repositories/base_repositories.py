from typing import TypeVar, Generic, Optional, Type, Any
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.sql import ColumnElement

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateType = TypeVar("CreateType", bound=SQLModel)


class BaseRepository(Generic[ModelType, CreateType]):

    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    async def get(self, _id: Any) -> Optional[ModelType]:
        return await self.db.get(self.model, _id)

    async def create(self, obj_in: CreateType) -> ModelType:
        if hasattr(obj_in, "model_dump"):
            obj_in = obj_in.model_dump()
        elif not isinstance(obj_in, dict):
            raise ValueError("obj_in 必须是 dict 或 Pydantic BaseModel")
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def list(self, skip: int = 0, limit: int = 20) -> list[ModelType]:
        stmt = select(self.model).offset(skip).limit(limit)
        result = await self.db.exec(stmt)
        return result.scalars().all()

    async def get_by_field(
            self,
            field: ColumnElement[Any],  # 🔥 关键修复点（不是 Any，不是 str）
            value: Any
    ) -> Optional[ModelType]:
        stmt = select(self.model).where(field == value).limit(1)
        result = await self.db.exec(stmt)
        return result.first()
