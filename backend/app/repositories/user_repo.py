from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.orm.user import User
from app.models.domain.user import UserCreate


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: UserCreate):
        user = User(email=data.email, name=data.name)
        if hasattr(data, 'password'):
            from app.core.security import get_password_hash
            user.hashed_password = get_password_hash(data.password)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def list_all(self):
        result = await self.db.execute(select(User))
        return result.scalars().all()

    async def get_by_email(self, email: str):
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalars().first()
