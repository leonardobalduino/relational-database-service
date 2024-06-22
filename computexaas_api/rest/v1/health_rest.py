from fastapi import APIRouter
from starlette import status

BASE_URL = "/api/v1/health"

router = APIRouter(
    prefix=BASE_URL,
    tags=["Health"],
    dependencies=[],
)


@router.get(
    "",
    name="Verifica se a aplicação está ok",
    description="Verifica se a aplicação está operante",
    status_code=status.HTTP_200_OK,
    response_model=str,
)
async def get_health():
    return "ok"
