from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import uuid4

from app.core.database import get_db
from app.models.motion import Motion
from app.core.dependencies import get_current_user
from app.core.permissions import require_roles
from app.enums.system_enums import UserRole

router = APIRouter(
    prefix="/motions",
    tags=["Motions"]
)

# =========================
# CREAR MOCIÓN
# =========================
@router.post("")
def create_motion(
    data: dict,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_roles([UserRole.ADMIN])(current_user)

    motion = Motion(
        id=uuid4(),
        title=data.get("title"),
        assembly_id=data.get("assembly_id")
    )

    db.add(motion)
    db.commit()
    db.refresh(motion)

    return motion


# =========================
# LISTAR MOCIONES
# =========================
@router.get("/{assembly_id}")
def list_motions(
    assembly_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(Motion).filter(
        Motion.assembly_id == assembly_id
    ).all()
