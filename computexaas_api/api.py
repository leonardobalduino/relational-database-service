from fastapi import FastAPI

from computexaas_api.configs.routes import config_routers


def init_fastapi_app() -> FastAPI:
    fastapi_app = FastAPI(
        title="Compute Xaas API",
        version="1.0.0",
        docs_url="/api/swagger",
        redoc_url="/api/docs",
    )

    return fastapi_app


def init_app():
    app = init_fastapi_app()
    config_routers(app)
    return app


app = init_app()
