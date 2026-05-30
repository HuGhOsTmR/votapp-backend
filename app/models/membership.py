from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid


class Membership(Base):
    __tablename__ = "memberships"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    assembly_id = Column(UUID(as_uuid=True), ForeignKey("assemblies.id"))

    role = Column(String, nullable=False)  # PRESIDENT, MEMBER, etc
    group = Column(String, nullable=True)
