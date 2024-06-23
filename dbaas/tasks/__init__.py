import asyncio
from enum import Enum
from functools import partial, wraps

from dbaas.configs.settings import settings

RETRY_KWARGS = {"max_retries": settings.celery.max_retries}


def run_in_new_loop(f):  # pragma: no cover
    def _get_loop():
        try:
            return asyncio.get_event_loop()
        except RuntimeError:
            return asyncio.new_event_loop()

    @wraps(f)
    def wrap(*args, **kwargs):
        p_func = partial(f, *args, **kwargs)
        event = _get_loop()
        ret = event.run_until_complete(p_func())
        return ret

    return wrap


@run_in_new_loop
async def call_service(fun, *args, **kwargs):
    return await fun(*args, **kwargs)


# O celery é sincrono, então precisa buscar o event loop para executar as tasks assincrona
async def run_in_executor(fnc, *args, **kwargs):
    loop = asyncio.get_event_loop()
    new_func = partial(fnc, *args, **kwargs)
    await loop.run_in_executor(None, new_func)


class Queue(str, Enum):
    DBAAS_PROVISION = "dbaas.provision.vm.1"
