from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

import uuid


class UserRole(Base):
    __tablename__ = "user_roles"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id")
    )

    role_id = Column(
        UUID(as_uuid=True),
        ForeignKey("roles.id")
    )