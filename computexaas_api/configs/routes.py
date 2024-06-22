from fastapi import FastAPI


def config_routers(app: FastAPI):
    from computexaas_api.rest.v1.health_rest import router as health
    from computexaas_api.rest.v1.provision_rest import router as provision

    routers = (health, provision)
    for rota in routers:
        app.include_router(rota)
