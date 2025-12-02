from typing import TypeVar, Generic, Optional, Type, Any, List
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

    async def create(self, obj_in: CreateType | dict) -> ModelType:
        data = obj_in.model_dump() if hasattr(obj_in, "model_dump") else obj_in
        db_obj = self.model(**data)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def list(self, skip: int = 0, limit: int = 20) -> List[ModelType]:
        stmt = select(self.model).offset(skip).limit(limit)
        result = await self.db.exec(stmt)
        return await result.scalars().all()

    async def get_by_field(
            self,
            field: ColumnElement[Any],
            value: Any
    ) -> Optional[ModelType]:

        stmt = select(self.model).where(field == value)
        result = await self.db.exec(stmt)
        return await result.one_or_none()

    async def delete(self, _id: Any) -> bool:
        obj = await self.get(_id)
        if not obj:
            return False
        await self.db.delete(obj)
        await self.db.commit()
        return True

    async def update(self, db_obj: ModelType, obj_in: dict | CreateType) -> ModelType:
        update_data = obj_in.model_dump(exclude_unset=True) \
            if hasattr(obj_in, "model_dump") else obj_in

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj
