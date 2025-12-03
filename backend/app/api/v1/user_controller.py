from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.core.exception import NotFoundException
from app.core.logger import get_logger
from app.services.user_service import UserService
from app.models.domain.user import UserCreate, UserOut
from app.utils.deps import get_user_service

router = APIRouter(prefix="/v1/users", tags=["users"])

logger = get_logger(__name__)


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, service: UserService = Depends(get_user_service)):
    logger.info(f" create user {payload}")
    if payload.name == 'string':
        raise NotFoundException("用不不存在")
    user = await service.create_user(payload)
    if not user:
        raise HTTPException(status_code=400, detail="Could not create user")
    logger.info(user)
    return user


@router.get("/", response_model=List[UserOut])
async def list_users(service: UserService = Depends(get_user_service)):
    return await service.list_users()
