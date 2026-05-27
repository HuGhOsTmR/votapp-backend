from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base

import uuid


class InstitutionRule(Base):
    __tablename__ = "institution_rules"

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

    rule_key = Column(
        String,
        nullable=False
    )

    rule_value = Column(
        Text,
        nullable=False
    )