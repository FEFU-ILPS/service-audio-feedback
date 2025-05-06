from contextlib import asynccontextmanager

from fastapi import FastAPI
from routers import health_router, feedback_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # on_startup

    yield

    # on_shutdown


service = FastAPI(lifespan=lifespan)

service.include_router(health_router)
service.include_router(feedback_router)
