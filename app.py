import hashlib
from contextlib import asynccontextmanager
from random import randbytes
from typing import Callable

from fastapi import FastAPI, Request

from routers import feedback_router, health_router
from service_logging import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    # До запуска приложения
    logger.info("FastAPI application starting up...")

    yield

    # После запуска
    logger.info("FastAPI application shutting down...")


service = FastAPI(lifespan=lifespan)


@service.middleware("http")
async def add_request_hash(request: Request, call_next: Callable):
    request_hash = hashlib.sha1(randbytes(32)).hexdigest()[:10]
    with logger.contextualize(request_hash=request_hash):
        response = await call_next(request)
        return response


service.include_router(health_router)
service.include_router(feedback_router)
