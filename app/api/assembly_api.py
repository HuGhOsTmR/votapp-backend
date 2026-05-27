from fastapi import (
    APIRouter,
    Depends
)

from app.core.dependencies import (
    get_current_user
)

from app.core.permissions import (
    require_roles
)

from app.enums.system_enums import UserRole

router = APIRouter(
    prefix="/assemblies",
    tags=["Assemblies"]
)


@router.post("/open")
def open_assembly(
    current_user = Depends(get_current_user)
):

    require_roles([
        UserRole.PRESIDENT
    ])(current_user)

    return {
        "message": "Sesión abierta correctamente"
    }