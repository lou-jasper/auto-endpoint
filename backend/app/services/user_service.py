from typing import List
from app.repositories.user_repo import UserRepository
from app.models.domain.user import UserCreate
from app.models.domain.user import UserOut


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def create_user(self, data: UserCreate) -> UserOut:
        user = await self.repo.create(data)
        return user

    async def list_users(self) -> List[UserOut]:
        return await self.repo.list_all()
