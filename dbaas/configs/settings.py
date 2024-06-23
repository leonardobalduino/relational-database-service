from enum import Enum

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class Environment(str, Enum):
    DEVELOPMENT = "DEVELOPMENT"
    TESTING = "TESTING"
    PRODUCTION = "PRODUCTION"


class MongoSettings(BaseModel):
    url_connection: str = Field("mongodb://localhost:27017/dbaas-db")


class RedisSettings(BaseModel):
    url_connection: str = Field("localhost")


class CelerySettings(BaseModel):
    task_always_eager: bool = Field(False)
    task_store_eager_result: bool = Field(False)
    broker_url: str = Field("amqp://user:password@localhost:5672")
    result_backend: str = Field("redis://localhost:6379/0")
    broker_connection_retry_on_startup: bool = Field(True)
    max_retries: int = Field(5)
    start_process_to_delete_instance_database_failures: int = Field(
        60, description="Schedule para excluir instancia com falha, em segundos"
    )


class ComputexaasApiSettings(BaseModel):
    url: str = Field("http://localhost:8001")
    timeout: int = Field(30)


class ApplicationSettings(BaseSettings):
    environment: Environment = Field(default=Environment.DEVELOPMENT)
    mongo: MongoSettings = Field(default=MongoSettings())
    redis: RedisSettings = Field(default=RedisSettings())
    celery: CelerySettings = Field(default=CelerySettings())
    computexaas_api: ComputexaasApiSettings = Field(default=CelerySettings())

    class Config:
        env_nested_delimiter = "__"


load_dotenv(verbose=True)

settings = ApplicationSettings()
