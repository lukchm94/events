from fastapi import APIRouter, status

from ..__app_configs import Paths

router = APIRouter(prefix=Paths.health.value, tags=[Paths.health_tag.value])


@router.get(Paths.root.value, status_code=status.HTTP_200_OK)
async def check_health() -> None:
    return {"status": "healthy"}
