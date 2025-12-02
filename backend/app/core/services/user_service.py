from typing import Any, Coroutine

from app.adapters.db.models.user_model import UserModel
from app.adapters.db.repositories.user_repositories import UserRepository
from app.api.v1.schemas.user_schema import UserCreate, UserUpdate


class UserService:
    @staticmethod
    async def create_user(db, data: UserCreate):
        repo = UserRepository(db)
        hashed_password = data.password
        user = UserModel(
            username=data.username,
            email=data.email,
            password_hash=hashed_password,
            is_active=True,
            is_superuser=False,
        )
        return await repo.create(user)

    @staticmethod
    async def get_user(db, user_id: str):
        repo = UserRepository(db)

        return await repo.get(user_id)

    @staticmethod
    async def update_user(db, user_id: str, data: UserUpdate):
        repo = UserRepository(db)

        user = await repo.get(user_id)
        if not user:
            return None

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(user, key, value)

        return await repo.update(user)

    @staticmethod
    async def delete_user(db, user_id: str) -> bool | Coroutine[Any, Any, bool]:
        repo = UserRepository(db)

        user = await repo.get(user_id)
        if not user:
            return False

        return repo.delete(user)
