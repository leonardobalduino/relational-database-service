import asyncio

from dbaas.configs.celery import celery
from dbaas.tasks import RETRY_KWARGS, Queue, call_service, run_in_executor


@celery.task(
    queue=Queue.DBAAS_PROVISION,
    name="start_process_instance_database_failures",
    autoretry_for=[Exception],
    retry_kwargs=RETRY_KWARGS,
)
def _start_process_instance_database_failures() -> dict[str, any] | None:
    from ..business.instance_database_bo import InstanceDataBaseTask

    return call_service(InstanceDataBaseTask().start_process_to_delete_instance_database_failures)


async def start_process_instance_database_failures():
    await asyncio.gather(run_in_executor(_start_process_instance_database_failures.delay, id))


@celery.task(
    queue=Queue.DBAAS_PROVISION,
    name="delete_instance_database_failed",
    autoretry_for=[Exception],
    retry_kwargs=RETRY_KWARGS,
)
def _delete_instance_database_failed(id: str) -> dict[str, any] | None:
    from ..business.instance_database_bo import InstanceDataBaseTask

    return call_service(InstanceDataBaseTask().delete_instance_database_failed, id)


async def delete_instance_database_failed(id: str):
    await asyncio.gather(run_in_executor(_delete_instance_database_failed.delay, id))
