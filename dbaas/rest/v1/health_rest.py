import asyncio
import logging

from fastapi import APIRouter, Response
from starlette import status

from dbaas.configs.mongo import client_mongo

BASE_URL = "/api/v1/health"

router = APIRouter(
    prefix=BASE_URL,
    tags=["Health"],
    dependencies=[],
)


@router.get(
    "",
    name="Verifica se a aplicação está ok",
    description="Verifica se a aplicação está operante e com acesso ao banco de dados",
    status_code=status.HTTP_200_OK,
    response_model=str,
)
async def get_health(response: Response):
    try:
        server_info = await asyncio.wait_for(client_mongo.server_info(), timeout=2.5)
        mongo_status = bool(server_info.get("ok", 0))
    except BaseException as e:  # NOSONAR
        logging.error("Falha ao conectar com o Mongo", exc_info=e)
        mongo_status = False

    response.status_code = status.HTTP_200_OK if mongo_status else status.HTTP_503_SERVICE_UNAVAILABLE

    return "ok" if mongo_status else "failed"
