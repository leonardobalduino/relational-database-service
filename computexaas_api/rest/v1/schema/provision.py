import random
import string
from datetime import datetime, timezone
from uuid import uuid4

from pydantic import BaseModel, Field

from computexaas_api.models.provision import AccessEnum, Address, Credencial, Provision


class ProvisionUtils:
    @staticmethod
    def random_ipv4():
        return ".".join(map(str, (random.randint(0, 255) for _ in range(4))))

    @staticmethod
    def generate_username(length=8):
        characters = string.ascii_letters + string.digits
        username = "".join(random.choice(characters) for _ in range(length))
        return username

    @staticmethod
    def generate_password(length=12):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = "".join(random.choice(characters) for _ in range(length))
        return password

    @staticmethod
    def random_region():
        regions = ["north", "northeast", "east", "southeast", "south", "southwest", "west", "northwest"]
        region = random.choice(regions)
        return region

    @staticmethod
    def utcnow():
        return datetime.now(timezone.utc)


class ProvisionResponse(Provision):
    @classmethod
    def create(cls, flavor: str, description: str, database: str) -> "Provision":
        provision = Provision(
            id=uuid4().hex,
            flavor=flavor,
            description=description,
            database=database,
            credencial=Credencial(
                user=ProvisionUtils.generate_username(),
                password=ProvisionUtils.generate_password(),
                access=list(AccessEnum),
            ),
            address=Address(
                ip=ProvisionUtils.random_ipv4(),
                region=ProvisionUtils.random_region(),
            ),
            created_at=ProvisionUtils.utcnow(),
            updated_at=ProvisionUtils.utcnow(),
        )
        return provision


class ProvisionRequest(BaseModel):
    flavor: str = Field(..., title="Flavor", examples=["667322e89a241357c97fcfd7"])
    description: str = Field(
        ..., title="Descrição do flavor", examples=["Pequeno (2 vCPUs; 4 GB RAM; 100 GB disco dados)"]
    )
    database: str = Field(..., title="Banco de dados", examples=["MYSQL"])


class ProvisionUpdateRequest(BaseModel):
    metadata: dict = Field(..., title="Metada")
