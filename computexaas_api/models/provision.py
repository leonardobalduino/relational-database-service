from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class AccessEnum(str, Enum):
    CREATE = "CREATE"
    READ = "READ"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


class Address(BaseModel):
    ip: str = Field(..., title="IP da base de dados", examples=["127.0.0.1"])
    region: str = Field(..., title="Região", examples=["Sudeste-1"])


class Credencial(BaseModel):
    user: str = Field(..., title="Usuário", examples=["foo"])
    password: str = Field(..., title="Senha", examples=["password"])
    access: list[AccessEnum] = Field(..., min_length=1, max_length=len(AccessEnum))


class Provision(BaseModel):
    id: str = Field(..., title="Identificador da VM provisionada", examples=["24380a0b60c4451b8d306ed871fe77da"])
    flavor: str = Field(..., title="Flavor", examples=["667322e89a241357c97fcfd7"])
    description: str = Field(
        ..., title="Descrição do flavor", examples=["Pequeno (2 vCPUs; 4 GB RAM; 100 GB disco dados)"]
    )
    database: str = Field(..., title="Banco de dados", examples=["MYSQL"])
    credencial: Credencial | None = Field(None, title="Credenciais do banco de dados")
    address: Address | None = Field(None, title="Endereço do banco de dados")
    created_at: datetime | None = Field(None, title="Data de criação")
    updated_at: datetime | None = Field(None, title="Data de alteração")
