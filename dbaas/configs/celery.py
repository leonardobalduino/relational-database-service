import logging

from celery import Celery, signals

from dbaas.configs.settings import settings

config_obj = {
    **settings.celery.model_dump(),
    "imports": ("dbaas.tasks.instance_database_tasks",),
}

CELERY_SCHEDULER = {
    "start_process_to_delete_instance_database_failures": {
        "task": "start_process_instance_database_failures",
        "schedule": settings.celery.start_process_to_delete_instance_database_failures,
    },
}

celery = Celery(**config_obj)
celery.conf.beat_schedule = CELERY_SCHEDULER


@signals.worker_process_shutdown.connect
def shutdown_worker(*args, **kwargs):  # pragma: no cover
    logging.info("Shutdown worker: (%s|%s)", args, kwargs)
