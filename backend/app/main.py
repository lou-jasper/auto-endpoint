from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, ResponseValidationError

from app.api.router import api_router
from app.core.exception import (
    global_exception_handler,
    validation_exception_handler,
    BusinessException,
    business_exception_handler,
    response_validation_exception_handler
)

from app.core.logger import configure_logging, request_id_middleware, get_logger, BestLogMiddleware
from app.lifespan import app_lifespan

configure_logging()

app = FastAPI(
    title="FastAPI MVCSR DDD Template",
    lifespan=app_lifespan,
)
app.middleware("http")(request_id_middleware)
app.add_middleware(BestLogMiddleware)

logger = get_logger(__name__)

app.include_router(api_router)

app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(BusinessException, business_exception_handler)
app.add_exception_handler(ResponseValidationError, response_validation_exception_handler)


@app.get("/ping")
async def ping():
    logger.info("ping called")
    return {"msg": "pong"}
