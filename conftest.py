import asyncio
import subprocess
import sys
from pathlib import Path

import pytest_asyncio

from dbaas.configs.mongo import client_mongo, database
from dbaas.configs.settings import Environment, settings

pytest_plugins = []


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()

    try:
        yield loop
    finally:
        loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def before_all():
    await _drop_default_database()
    _execute_migrations()
    pass


@pytest_asyncio.fixture(autouse=True)
async def before_after_each():
    await _before_each()
    yield None


async def _before_each():
    await _clear_collections()


async def _drop_default_database():
    await client_mongo.drop_database(database)


async def _clear_collections():
    for collection_name in await database.list_collection_names():
        await database[collection_name].delete_many({})


def _ensure_testing_environment():
    env = settings.environment

    if env != Environment.TESTING:  # pragma: no cover
        print(
            f"❌ '{env.name}' não é um ambiente de testes.\n"
            f"Para carregar o ambiente de testes execute `make load-test-env` ou `cp devtools/env/dotenv.test .env`",
            file=sys.stderr,
        )
        sys.exit(1)


def _execute_migrations():
    result = _run_migration_make_target()

    if result.returncode != 0:  # pragma: no cover
        msg = result.stderr.decode("utf-8")
        print("❌ Falha ao executar migrações:", msg, file=sys.stderr)
        sys.exit(1)


def _run_migration_make_target():
    db_uri = settings.mongo.url_connection
    cmd = ["mongodb-migrate", "--url", f"{db_uri}", "--migrations", "migrations"]
    project_root_dir = Path(__file__).parent
    result = subprocess.run(cmd, cwd=project_root_dir, stderr=subprocess.PIPE)
    return result


_ensure_testing_environment()
