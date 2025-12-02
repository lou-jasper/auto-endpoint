from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.adapters.db.models.user_model import UserModel
from app.adapters.db.repositories.base_repositories import BaseRepository


class UserRepository(BaseRepository):

    def __init__(self, db: AsyncSession):
        super().__init__(UserModel, db)

    async def get_by_email(self, email: str) -> UserModel | None:
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def update(self, user: UserModel, **update_data) -> UserModel:
        """
        使用 BaseModel.update() 自动过滤字段并更新 updated_at。
        update_data 仅包含需要更新的字段。
        """
        # 使用 BaseModel 的 update 方法（异步，但仅字段更新）
        await user.update(**update_data)

        # 写入数据库
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete(self, user: UserModel) -> bool:
        await self.db.delete(user)
        await self.db.commit()
        return True
