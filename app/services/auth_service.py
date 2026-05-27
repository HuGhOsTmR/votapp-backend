from sqlalchemy.orm import Session
from app.models.user import User

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)


def register_user(
    db: Session,
    full_name: str,
    email: str,
    password: str,
    institution_id
):
    hashed = hash_password(password)

    user = User(
        full_name=full_name,
        email=email,
        password_hash=hashed,
        institution_id=institution_id
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(
    db: Session,
    email: str,
    password: str
):
    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        return None

    if not verify_password(
        password,
        user.password_hash
    ):
        return None

    token = create_access_token({
        "sub": str(user.id),
        "email": user.email
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }

def get_user_by_id(
    db: Session,
    user_id
):
    return db.query(User).filter(
        User.id == user_id
    ).first()