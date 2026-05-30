from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    Enum
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship

from app.core.database import Base

from app.enums.system_enums import UserRole

import uuid

from datetime import datetime


class User(Base):

    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    institution_id = Column(
        UUID(as_uuid=True),
        ForeignKey("institutions.id"),
        nullable=True
    )

    full_name = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        nullable=False
    )

    password_hash = Column(
        String,
        nullable=False
    )

    role = Column(
        Enum(UserRole),
        default=UserRole.ASSEMBLY_MEMBER,
        nullable=False
    )
    party = Column(String, default="OTROS")
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    institution = relationship(
        "Institution",
        backref="users"
    )
    attendance_records = relationship(
    "Attendance",
    back_populates="user"
    )

    group_id = Column(
        UUID(as_uuid=True),
        ForeignKey("groups.id"),
        nullable=True
    )

    group = relationship("Group")
    memberships = relationship("Membership", backref="user")
