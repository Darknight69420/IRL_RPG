from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base

class Creature(Base):
    __tablename__ = "creatures"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    species_id = Column(Integer, ForeignKey("species.id"), nullable=False)
    nickname = Column(String(50), nullable=False)
    level = Column(Integer, default=1, nullable=False)
    current_xp = Column(Integer, default=0, nullable=False)
    bond_score = Column(Integer, default=10, nullable=False) # 0 - 100
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    user = relationship("User", back_populates="creatures")
    species = relationship("Species", back_populates="creatures")

class CollectionEntry(Base):
    __tablename__ = "collection_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    species_id = Column(Integer, ForeignKey("species.id"), nullable=False)
    status = Column(String(20), default="AWAKENED", nullable=False) # DISCOVERED, AWAKENED
    unlocked_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "species_id", name="uq_user_species_collection"),
    )

    user = relationship("User", back_populates="collection_entries")
    species = relationship("Species", back_populates="collection_entries")
