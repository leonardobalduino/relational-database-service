# from enum import Enum

from typing import Literal

from pydantic import Field

from dbaas.models.base_model import BaseId, BaseModel
from dbaas.models.instance_database import DatabaseEnum, InstanceDatabaseBase, StatusEnum


class InstanceDatabaseRequest(BaseModel):
    flavor_id: str = Field(..., title="Identificador do flavor", examples=["667322e89a241357c97fcfd7"])
    database: DatabaseEnum = Field(..., title="Tipo de banco de dados", examples=[DatabaseEnum.POSTGRESQL])


class InstanceDatabaseRespose(InstanceDatabaseBase, BaseId):
    flavor_id: str = Field(..., title="Identificador do flavor", examples=["667322e89a241357c97fcfd7"])
    database: DatabaseEnum = Field(..., title="Tipo de banco de dados", examples=[DatabaseEnum.POSTGRESQL])


class InstanceDatabaseStatusRequest(BaseModel):
    status: Literal[StatusEnum.ACTIVE, StatusEnum.STOPPED] = Field(
        ..., title="Status do banco de dados", examples=[StatusEnum.ACTIVE]
    )
