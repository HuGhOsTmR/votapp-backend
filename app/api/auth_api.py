from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user
from app.schemas.auth_schema import (
    UserCreate,
    UserLogin
)

from app.services.auth_service import (
    register_user,
    authenticate_user
)

from app.core.database import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
    data: UserCreate,
    db: Session = Depends(get_db)
):

    user = register_user(
        db=db,
        full_name=data.full_name,
        email=data.email,
        password=data.password,
        institution_id=None
    )

    return {
        "message": "Usuario registrado",
        "user_id": str(user.id)
    }


@router.post("/login")
def login(
    data: UserLogin,
    db: Session = Depends(get_db)
):

    result = authenticate_user(
        db=db,
        email=data.email,
        password=data.password
    )

    if not result:
        return {
            "error": "Credenciales inválidas"
        }

    return result

@router.get("/me")
def get_me(
    current_user = Depends(get_current_user)
):

    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "role": current_user.role
    }