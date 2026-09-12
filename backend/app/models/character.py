from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base

class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    level = Column(Integer, default=1, nullable=False)
    current_xp = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    user = relationship("User", back_populates="character")
    attributes = relationship("CharacterAttribute", back_populates="character", cascade="all, delete-orphan")

class CharacterAttribute(Base):
    __tablename__ = "character_attributes"

    id = Column(Integer, primary_key=True, index=True)
    character_id = Column(Integer, ForeignKey("characters.id", ondelete="CASCADE"), nullable=False, index=True)
    code = Column(String(10), nullable=False) # STR, INT, WIS, DIS, VIT, CHA
    value = Column(Float, default=0.0, nullable=False)

    __table_args__ = (
        UniqueConstraint("character_id", "code", name="uq_character_attribute"),
    )

    character = relationship("Character", back_populates="attributes")
