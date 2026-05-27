from fastapi import HTTPException, Depends
from app.core.dependencies import get_current_user
from app.enums.system_enums import UserRole


def require_roles(allowed_roles: list):

    def validator(current_user = Depends(get_current_user)):

        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="No autorizado"
            )

        return current_user

    return validator