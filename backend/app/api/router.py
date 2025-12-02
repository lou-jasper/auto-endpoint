from fastapi import APIRouter

from app.api.v1.endpoints.cache import router as cache_router
from app.api.v1.endpoints.user import router as user_router

api_router = APIRouter()

api_router.include_router(cache_router)
api_router.include_router(user_router)
