from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Enum
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship

from app.core.database import Base

from app.enums.system_enums import AttendanceStatus

import uuid

from datetime import datetime


class Attendance(Base):

    __tablename__ = "attendance"

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

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    status = Column(
        Enum(AttendanceStatus),
        default=AttendanceStatus.CONNECTED,
        nullable=False
    )

    connected_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    disconnected_at = Column(DateTime)

    # RELACIÓN CON USER
    user = relationship(
        "User",
        back_populates="attendance_records"
    )

    # RELACIÓN CON ASSEMBLY
    assembly = relationship(
        "Assembly",
        back_populates="attendances"
    )