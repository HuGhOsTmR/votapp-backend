from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.enums.system_enums import MotionStatus

import uuid
from datetime import datetime


class Motion(Base):
    __tablename__ = "motions"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    assembly_id = Column(
        UUID(as_uuid=True),
        ForeignKey("assemblies.id"),
        nullable=False
    )

    created_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    title = Column(String, nullable=False)

    description = Column(Text)

    status = Column(
        Enum(MotionStatus),
        default=MotionStatus.PROPOSED,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    # 🔥 NUEVO
    closed_at = Column(
        DateTime,
        nullable=True
    )

    # relaciones
    votes = relationship(
        "Vote",
        backref="motion"
    )

    amendments = relationship(
        "Amendment",
        backref="motion"
    )

    assembly = relationship(
        "Assembly",
        back_populates="motions"
    )