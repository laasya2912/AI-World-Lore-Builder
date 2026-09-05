from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from database import Base


class Lore(Base):
    __tablename__ = "lore"

    id = Column(Integer, primary_key=True, index=True)
    world_id = Column(Integer, nullable=False)
    type = Column(String(50), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    facts = Column(Text, nullable=True)
    relationships = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )