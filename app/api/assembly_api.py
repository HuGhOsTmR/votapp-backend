from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import uuid4

from app.core.database import get_db
from app.models.assembly import Assembly
from app.core.dependencies import get_current_user
from app.core.permissions import require_roles
from app.enums.system_enums import UserRole

router = APIRouter(
    prefix="/assemblies",
    tags=["Assemblies"]
)

# =========================
# CREAR ASAMBLEA
# =========================
@router.post("")
def create_assembly(
    data: dict,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_roles([UserRole.ADMIN])(current_user)

    assembly = Assembly(
        id=uuid4(),
        name=data.get("name"),
        type=data.get("type")
    )

    db.add(assembly)
    db.commit()
    db.refresh(assembly)

    return assembly


# =========================
# LISTAR ASAMBLEAS
# =========================
@router.get("")
def list_assemblies(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(Assembly).all()


# =========================
# ABRIR SESIÓN (lo que ya tenías)
# =========================
@router.post("/open")
def open_assembly(
    current_user=Depends(get_current_user)
):
    require_roles([UserRole.PRESIDENT])(current_user)

    return {
        "message": "Sesión abierta correctamente"
    }
