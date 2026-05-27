from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Enum,
    Boolean,
    UniqueConstraint
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.enums.system_enums import VoteValue

import uuid
from datetime import datetime


class Vote(Base):
    __tablename__ = "votes"

    __table_args__ = (
        UniqueConstraint(
            "motion_id",
            "user_id",
            "is_current",
            name="uq_active_vote"
        ),
    )

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    motion_id = Column(
        UUID(as_uuid=True),
        ForeignKey("motions.id"),
        nullable=False
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    vote_value = Column(
        Enum(VoteValue),
        nullable=False
    )

    is_current = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    user = relationship(
        "User",
        backref="votes"
    )

    history = relationship(
        "VoteHistory",
        backref="vote"
    )