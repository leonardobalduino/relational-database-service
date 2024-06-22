from fastapi import APIRouter
from starlette import status

from dbaas.business.flavor_bo import FlavorBusiness
from dbaas.rest.v1.schema.flavor import FlavorResponse

BASE_URL = "/api/v1/flavors"

router = APIRouter(
    prefix=BASE_URL,
    tags=["Flavors"],
    dependencies=[],
)


@router.get(
    "",
    name="Lista os flavors",
    description="Realiza a busca de flavors",
    status_code=status.HTTP_200_OK,
    response_model=list[FlavorResponse],
    response_model_by_alias=False,
)
async def get_flavors():
    results = await FlavorBusiness().find_all()
    return results
