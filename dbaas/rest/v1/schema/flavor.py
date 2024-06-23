from pydantic import Field, model_validator

from dbaas.models.base_model import BaseId
from dbaas.models.flavor import FlavorBase


class FlavorResponse(FlavorBase, BaseId):
    description: str | None = Field(
        None, title="Descrição do flavor", examples=["Pequeno (2 vCPUs; 4 GB RAM; 100GB disco dados)"]
    )

    @model_validator(mode="after")
    def set_description(cls, values):
        values.description = "{name} ({vcpu} vCPUs; {ram} GB RAM; {disc} GB disco dados)".format(
            name=values.name, vcpu=values.vcpu, ram=values.ram, disc=values.disc
        )
        return values
