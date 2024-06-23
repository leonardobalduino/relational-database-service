import logging
from typing import TYPE_CHECKING

from dbaas.business.flavor_bo import FlavorBusiness
from dbaas.exceptions.exception import (
    BadRequestException,
    NotFoundException,
    TimeoutException,
    UnprocessableEntityException,
)
from dbaas.integrations.computexaas_api import ComputexaasApi
from dbaas.models.instance_database import InstanceDatabase, StatusEnum
from dbaas.repositories.instance_database_repository import InstanceDataBaseRepository

if TYPE_CHECKING:
    from dbaas.rest.v1.schema.instance_database import InstanceDatabaseRequest


class InstanceDataBaseBusiness:
    def __init__(self):
        self.instance_database_repository = InstanceDataBaseRepository(InstanceDatabase)
        self.flavor_bo = FlavorBusiness()

    def is_active_or_stopped(self, instance_database: InstanceDatabase) -> bool:
        return instance_database.status in (StatusEnum.ACTIVE, StatusEnum.STOPPED)

    async def find_all(self) -> list[InstanceDatabase]:
        result = await self.instance_database_repository.find_all()
        return result

    async def find_by_filter(self, filter: dict) -> list[InstanceDatabase]:
        result = await self.instance_database_repository.find_by_filter(filter)
        return result

    async def find_all_failures(
        self,
    ) -> list[InstanceDatabase]:
        result = await self.instance_database_repository.find_by_filter({"status": StatusEnum.FAILED})
        return result

    async def create(self, instance_database: "InstanceDatabaseRequest") -> InstanceDatabase:
        instance_database_provision = InstanceDatabase(
            flavor_id=instance_database.flavor_id,
            database=instance_database.database,
            status=StatusEnum.PROVISIONING,
        )
        created = await self.instance_database_repository.create(instance_database_provision)
        return created

    async def update(self, instancedata_base: InstanceDatabase) -> InstanceDatabase:
        if not (updated := await self.instance_database_repository.update(instancedata_base)):
            raise UnprocessableEntityException("Não foi possível atualizar a instancia da base")
        return updated

    async def get_by_id(self, id: str, throw_exception: bool = True) -> InstanceDatabase:
        if not (result := await self.instance_database_repository.get_by_id(id)) and throw_exception:
            raise NotFoundException("Instância de dados não encontrado")
        return result

    async def delete_by_id(self, id: str) -> bool:
        return await self.instance_database_repository.delete_by_id(id)

    async def update_status(self, instancedata_base: InstanceDatabase, status: StatusEnum) -> InstanceDatabase:
        instancedata_base.status = status
        updated = await self.update(instancedata_base)
        return updated

    async def provision_database(self, instance_database: "InstanceDatabaseRequest") -> InstanceDatabase:
        flavor = await self.flavor_bo.get_by_id(instance_database.flavor_id)
        instance_created = await self.create(instance_database)

        try:
            provision = await ComputexaasApi.provision_vm(
                flavor.id, flavor.get_description(flavor), instance_created.database
            )
            instance_created.provision = provision
            instance_update = await self.update_status(instance_created, StatusEnum.STOPPED)
            return instance_update
        except TimeoutException as e:
            """
            Uma rotina em backgroud vai fazer uma chamada para ComputeXaaS
            para excluir o provisonamento e depois excluir a instancia criada no DBaaS
            """
            instance_update = await self.update_status(instance_created, StatusEnum.FAILED)
            raise e
        except Exception as e:
            # Excluir para não ficar lixo na base de dados
            await self.delete_by_id(instance_created.id)
            logging.error("excluido instancia sem provisionamento", exc_info=e)
            raise BadRequestException(
                "Não foi possível provisinar instancia de base da dados no momento, tente mais tarde"
            )

    async def provision_delete(self, id: str) -> None:
        instance_database = await self.get_by_id(id)
        if not self.is_active_or_stopped(instance_database):
            raise BadRequestException(
                f"Não é possível excluir instancia de banco de dados no status atual `{instance_database.status.value}`"
            )

        await self.provision_delete_vm(instance_database)

    async def provision_delete_vm(self, instance_database: InstanceDatabase) -> None:
        try:
            if await ComputexaasApi.provision_delete(instance_database.id):
                await self.delete_by_id(instance_database.id)
        except TimeoutException:
            """
            Uma rotina em backgroud vai fazer uma chamada para ComputeXaaS
            para excluir o provisonamento e depois excluir a instancia criada no DBaaS
            """
            await self.update_status(instance_database, StatusEnum.FAILED)
            raise
        except Exception as e:
            logging.error("excluido instancia", exc_info=e)
            raise BadRequestException(
                "Não foi possível excluir instancia de base da dados no momento, tente mais tarde"
            )

    async def set_as_active_or_stopped(self, id: str, status: StatusEnum) -> InstanceDatabase:
        instance_database = await self.get_by_id(id)
        if not self.is_active_or_stopped(instance_database):
            raise BadRequestException(
                f"Não é possível mudar o status da instancia de banco de dados no status atual `{instance_database.status.value}`"
            )

        if instance_database.status == status:
            raise BadRequestException(
                f"Instancia de banco de dados já se encontra no status atual `{instance_database.status.value}`"
            )

        updated = await self.update_status(instance_database, status)
        return updated


class InstanceDataBaseTask(InstanceDataBaseBusiness):
    async def start_process_to_delete_instance_database_failures(self):
        from dbaas.tasks import instance_database_tasks as task

        failures = await self.find_all_failures()
        for failed in failures:
            await task.delete_instance_database_failed(failed.id)

    async def delete_instance_database_failed(self, id: str):
        instance_database = await self.get_by_id(id, False)
        if not instance_database or instance_database.status != StatusEnum.FAILED:
            return {
                "id": id,
                "detail": {
                    "msg": "não pode ser excluido",
                    "error": (
                        f"status atual `{instance_database.status}`"
                        if instance_database
                        else "instancia não encontrada"
                    ),
                },
            }

        await self.provision_delete_vm(instance_database)
