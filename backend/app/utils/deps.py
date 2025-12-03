from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal
from app.repositories.user_repo import UserRepository
from app.services.user_service import UserService


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


def get_user_service(db=Depends(get_db)):
    repo = UserRepository(db)
    return UserService(repo)
