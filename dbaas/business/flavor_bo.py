from dbaas.exceptions.exception import NotFoundException
from dbaas.models.flavor import Flavor
from dbaas.repositories.flavor_repository import FlavorRepository


class FlavorBusiness:
    def __init__(self):
        self.flavor_repository = FlavorRepository(Flavor)

    async def get_by_id(self, id) -> Flavor:
        if not (result := await self.flavor_repository.get_by_id(id)):
            raise NotFoundException("Flavor não encontrado")
        return result

    async def find_all(self) -> list[Flavor]:
        result = await self.flavor_repository.find_all()
        return result
