from contextlib import asynccontextmanager

from fastapi import FastAPI

from dbaas.configs.mongo import client_mongo
from dbaas.configs.routes import config_routers


def shutdown_mongo():
    client_mongo.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    ...
    yield
    shutdown_mongo()


def init_fastapi_app() -> FastAPI:
    fastapi_app = FastAPI(
        title="Database as a Service API",
        version="1.0.0",
        docs_url="/api/swagger",
        redoc_url="/api/docs",
        lifespan=lifespan,
    )
    config_routers(fastapi_app)
    return fastapi_app


def init_app():
    app = init_fastapi_app()
    return app


app = init_app()
