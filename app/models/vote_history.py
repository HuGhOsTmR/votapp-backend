from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

import uuid
from datetime import datetime


class VoteHistory(Base):
    __tablename__ = "vote_history"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    vote_id = Column(
        UUID(as_uuid=True),
        ForeignKey("votes.id")
    )

    previous_value = Column(String)

    new_value = Column(String)

    changed_at = Column(
        DateTime,
        default=datetime.utcnow
    )