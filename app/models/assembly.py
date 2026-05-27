from sqlalchemy import Column, String, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.enums.system_enums import AssemblyStatus

import uuid
from datetime import datetime


class Assembly(Base):
    __tablename__ = "assemblies"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    institution_id = Column(
        UUID(as_uuid=True),
        ForeignKey("institutions.id"),
        nullable=False
    )

    title = Column(String, nullable=False)

    status = Column(
        Enum(AssemblyStatus),
        default=AssemblyStatus.DRAFT,
        nullable=False
    )

    started_at = Column(DateTime)

    ended_at = Column(DateTime)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    institution = relationship(
        "Institution",
        back_populates="assemblies"
    )

    motions = relationship(
        "Motion",
        back_populates="assembly"
    )

    attendances = relationship(
    "Attendance",
    back_populates="assembly"
    )

    groups = relationship(
        "Group",
        back_populates="assembly"
    )