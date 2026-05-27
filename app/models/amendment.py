from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

import uuid
from datetime import datetime


class Amendment(Base):
    __tablename__ = "amendments"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    motion_id = Column(
        UUID(as_uuid=True),
        ForeignKey("motions.id")
    )

    created_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id")
    )

    content = Column(Text)

    status = Column(
        String,
        default="proposed"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )