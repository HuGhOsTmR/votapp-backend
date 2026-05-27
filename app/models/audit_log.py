from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

import uuid
from datetime import datetime


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True
    )

    action = Column(String, nullable=False)

    entity_type = Column(String)

    entity_id = Column(String)

    details = Column(Text)

    ip_address = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )