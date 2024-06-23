from enum import Enum

from pydantic import Field

from dbaas.models.base_model import Auditable, BaseId, BaseModel


class StatusEnum(str, Enum):
    ACTIVE = "ACTIVE"
    STOPPED = "STOPPED"
    PROVISIONING = "PROVISIONING"
    FAILED = "FAILED"


class DatabaseEnum(str, Enum):
    AURORA_MYSQL = "AURORA_MYSQL"
    AURORA_POSTGRESQL = "AURORA_POSTGRESQL"
    MARIADB = "MARIADB"
    MYSQL = "MYSQL"
    POSTGRESQL = "POSTGRESQL"
    ORACLE = "ORACLE"
    MICROSOFT_SQL_SERVER = "MICROSOFT_SQL_SERVER"
    IBM_DB2 = "IBM_DB2"


class InstanceDatabaseBase(BaseModel):
    flavor_id: str = Field(..., title="Identificador do flavor", examples=["667322e89a241357c97fcfd7"])
    database: DatabaseEnum = Field(..., title="Tipo de banco de dados", examples=[DatabaseEnum.POSTGRESQL])
    status: StatusEnum = Field(..., title="Status da instancia de banco de dados", examples=[StatusEnum.PROVISIONING])
    provision: dict | None = Field(None, title="Provisionamento do banco de dados")


class InstanceDatabase(Auditable, InstanceDatabaseBase, BaseId): ...
