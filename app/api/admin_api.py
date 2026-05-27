from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user
from app.core.permissions import require_roles
from app.enums.system_enums import UserRole
router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/test")
def admin_test(user = Depends(require_roles([UserRole.ADMIN]))):
    return {"message": "Acceso permitido ADMIN"}