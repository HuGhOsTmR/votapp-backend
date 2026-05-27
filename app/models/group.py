

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base
import uuid


class Group(Base):
    __tablename__ = "groups"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String, nullable=False)   
    type = Column(String, nullable=False)   

    color = Column(String, default="#cccccc")  # 🎨 para UI

    assembly_id = Column(
        UUID(as_uuid=True),
        ForeignKey("assemblies.id"),
        nullable=False
    )

    assembly = relationship("Assembly", back_populates="groups")