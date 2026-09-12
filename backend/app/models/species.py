from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class Species(Base):
    __tablename__ = "species"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    archetype = Column(String(100), nullable=False)
    tier = Column(Integer, nullable=False, index=True) # 1, 2, 3
    dominant_attribute = Column(String(10), nullable=True) # STR, INT, WIS, etc.
    description = Column(Text, nullable=False)
    sprite_asset_key = Column(String(100), nullable=False)

    creatures = relationship("Creature", back_populates="species")
    collection_entries = relationship("CollectionEntry", back_populates="species")
