from fastapi import FastAPI


def config_routers(app: FastAPI):
    from dbaas.rest.v1.flavor_rest import router as flavors
    from dbaas.rest.v1.health_rest import router as health
    from dbaas.rest.v1.instance_database_rest import router as instance_database

    routers = (health, flavors, instance_database)
    for rota in routers:
        app.include_router(rota)
