from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


# =========================
# WORLD
# =========================

class World(Base):
    __tablename__ = "worlds"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    genre = Column(String)

    tone = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)

    lore = relationship(
        "Lore",
        back_populates="world",
        cascade="all, delete-orphan"
    )


# =========================
# LORE
# =========================

class Lore(Base):
    __tablename__ = "lore"

    id = Column(Integer, primary_key=True, index=True)

    world_id = Column(
        Integer,
        ForeignKey("worlds.id"),
        nullable=False
    )

    # REGION / FACTION / CHARACTER / EVENT
    type = Column(String, nullable=False)

    name = Column(String, nullable=False)

    description = Column(Text)

    metadata_json = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    world = relationship(
        "World",
        back_populates="lore"
    )


# =========================
# RELATIONSHIPS
# =========================

class LoreRelationship(Base):
    __tablename__ = "relationships"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    source_id = Column(
        Integer,
        ForeignKey("lore.id"),
        nullable=False
    )

    target_id = Column(
        Integer,
        ForeignKey("lore.id"),
        nullable=False
    )

    relationship_type = Column(
        String,
        nullable=False
    )


# =========================
# BRANCHES
# =========================

class LoreBranch(Base):
    __tablename__ = "branches"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    world_id = Column(
        Integer,
        ForeignKey("worlds.id"),
        nullable=False
    )

    parent_lore_id = Column(
        Integer,
        ForeignKey("lore.id"),
        nullable=True
    )

    name = Column(
        String,
        nullable=False
    )

    description = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )