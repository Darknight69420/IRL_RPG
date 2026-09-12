from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(20), default="HABIT", nullable=False) # HABIT, TASK
    difficulty = Column(String(20), default="MEDIUM", nullable=False) # TRIVIAL, EASY, MEDIUM, HARD, HEROIC
    primary_attribute = Column(String(10), nullable=False) # STR, INT, WIS, DIS, VIT, CHA
    secondary_attribute = Column(String(10), nullable=True) # STR, INT, etc.
    cooldown_hours = Column(Integer, default=24, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    last_completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    user = relationship("User", back_populates="activities")
