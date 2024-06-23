from fastapi import APIRouter
from starlette import status

from dbaas.business.instance_database_bo import InstanceDataBaseBusiness
from dbaas.rest.v1.schema.instance_database import (
    InstanceDatabaseRequest,
    InstanceDatabaseRespose,
    InstanceDatabaseStatusRequest,
)

BASE_URL = "/api/v1/instance-databases"

router = APIRouter(
    prefix=BASE_URL,
    tags=["Instance Database"],
    dependencies=[],
)


@router.post(
    "",
    name="Cria instancia de banco de dados",
    description="Realiza a criação de instancia de banco de dados",
    status_code=status.HTTP_201_CREATED,
    response_model=InstanceDatabaseRespose,
)
async def create_instance_database(instance_database: InstanceDatabaseRequest):
    created = await InstanceDataBaseBusiness().provision_database(instance_database)
    return created


@router.get(
    "",
    name="Lista as instancias de banco de dados",
    description="Realiza a busca de instancias de banco de dados",
    status_code=status.HTTP_200_OK,
    response_model=list[InstanceDatabaseRespose],
    response_model_by_alias=False,
)
async def get_instance_database():
    results = await InstanceDataBaseBusiness().find_all()
    return results


@router.delete(
    "/{id}",
    name="Excluir instancia de banco de dados",
    description="Realiza a exclusão de instancia de banco de dados",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_instance_database(id: str):
    await InstanceDataBaseBusiness().provision_delete(id)


@router.put(
    "{id}/status",
    name="Alterar o status instancia do banco de dados",
    description="Realiza a alteração do status da instancias de banco de dados",
    status_code=status.HTTP_200_OK,
    response_model=InstanceDatabaseRespose,
    response_model_by_alias=False,
)
async def update_status_instance_database(id: str, status: InstanceDatabaseStatusRequest):
    updated = await InstanceDataBaseBusiness().set_as_active_or_stopped(id, status.status)
    return updated
