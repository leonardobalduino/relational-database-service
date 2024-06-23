import logging

import httpx
from starlette import status

from dbaas.configs.settings import settings
from dbaas.exceptions.exception import TimeoutException


class ComputexaasApi:
    @staticmethod
    async def provision_vm(flavor_id: str, description: str, database: str) -> dict:
        async with httpx.AsyncClient() as session:
            url = f"{settings.computexaas_api.url}/api/v1/provisions"

            try:
                response = await session.post(
                    url,
                    json={"flavor": flavor_id, "description": description, "database": database},
                    timeout=settings.computexaas_api.timeout,
                )
                response.raise_for_status()
                body = response.json()
                return body
            except httpx.TimeoutException as e:
                logging.error("timeout no provisionamento da vm no compute xaas api", exc_info=e)
                raise TimeoutException(detail="não foi possivel provisionar VM")
            except Exception as e:
                logging.error("nao foi possivel provisonar vm no compute xaas api", exc_info=e)
                raise e

    @staticmethod
    async def provision_delete(external_id: str) -> bool:
        async with httpx.AsyncClient() as session:
            url = f"{settings.computexaas_api.url}/api/v1/provisions/external/{external_id}"

            try:
                response = await session.delete(url)
                response.raise_for_status()
                return response.status_code == status.HTTP_204_NO_CONTENT
            except httpx.TimeoutException as e:
                logging.error("timeout na exclusão do provisionamento da vm no compute xaas api", exc_info=e)
                raise httpx.TimeoutException()
            except Exception as e:
                logging.error("nao foi possivel  excluir provisonar vm no compute xaas api", exc_info=e)
                raise e
