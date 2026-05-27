from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime


class Institution(Base):
    __tablename__ = "institutions"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    name = Column(String, nullable=False)

    acronym = Column(String, nullable=True)

    status = Column(String, default="active")

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
    assemblies = relationship(
    "Assembly",
    back_populates="institution"
    )