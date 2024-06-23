from pydantic import Field, model_validator

from dbaas.models.base_model import Auditable, BaseId, BaseModel


class FlavorBase(BaseModel):
    name: str = Field(..., title="Nome do flavor", examples=["Pequeno"])
    vcpu: int = Field(..., title="Quantidade de vCPU", examples=[2])
    ram: int = Field(..., title="Quantidade de RAM", examples=[4])
    disc: int = Field(..., title="Tamanho do disco", examples=[100])


class Flavor(Auditable, FlavorBase, BaseId):

    @staticmethod
    def get_description(values) -> str:
        _description = "{name} ({vcpu} vCPUs; {ram} GB RAM; {disc} GB disco dados)".format(
            name=values.name, vcpu=values.vcpu, ram=values.ram, disc=values.disc
        )
        return _description


class FlavorResponse(FlavorBase, BaseId):
    description: str | None = Field(
        None, title="Descrição do flavor", examples=["Pequeno (2 vCPUs; 4 GB RAM; 100GB disco dados)"]
    )

    @model_validator(mode="after")
    def set_description(cls, values):
        values.description = Flavor.get_description(values)
        return values
