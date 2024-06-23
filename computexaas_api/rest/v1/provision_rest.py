import asyncio
import logging
import random

from fastapi import APIRouter
from starlette import status

from computexaas_api.rest.v1.schema.provision import ProvisionRequest, ProvisionResponse, ProvisionUpdateRequest

BASE_URL = "/api/v1/provisions"

router = APIRouter(
    prefix=BASE_URL,
    tags=["Provisions"],
    dependencies=[],
)


@router.post(
    "",
    name="Provisiona VM para instância banco de dados",
    description="Realiza o provisionamento para uma instância de banco de dados",
    status_code=status.HTTP_201_CREATED,
    response_model=ProvisionResponse,
)
async def provision(provision: ProvisionRequest):
    # Simula o tempo de espera para causar o timeout para o DBaas
    await asyncio.sleep(random.randint(1, 60))

    # Criar uma VM Fake
    provisionated = ProvisionResponse.create(
        flavor=provision.flavor,
        description=provision.description,
        database=provision.database,
    )
    return provisionated


@router.delete(
    "/external/{external_id}",
    name="Excluir o provisonamento de VM para instância de banco de dados",
    description="Realiza a excluição de de provisionamento de VM para instância de banco de dados",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_provision(external_id: str):
    # Delete Fake
    logging.info(f"provisionamento '{external_id}' excluido")


@router.put(
    "/{id}",
    name="Alterar provisionamento de VM para instância de banco de dados",
    description="Realiza a alteração do provisionamento de VM para instância de banco de dados",
    status_code=status.HTTP_200_OK,
)
async def update_provision(provision: ProvisionUpdateRequest):
    # Alteração Fake
    logging.info(f"provisionamento '{provision}' alterado")
    return provision
