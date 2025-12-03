from fastapi import APIRouter
from app.api.v1.user_controller import router as user_router
from app.api.v1.redis_controller import router as redis_router

api_router = APIRouter(prefix="/api")
api_router.include_router(user_router)
api_router.include_router(redis_router)
