from enum import Enum

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings


class Environment(str, Enum):
    DEVELOPMENT = "DEVELOPMENT"
    TESTING = "TESTING"
    PRODUCTION = "PRODUCTION"


class ApplicationSettings(BaseSettings):
    environment: Environment = Field(default=Environment.DEVELOPMENT)

    class Config:
        env_nested_delimiter = "__"


load_dotenv(verbose=True)

settings = ApplicationSettings()
