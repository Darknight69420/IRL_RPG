from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class ChronicleEvent(Base):
    __tablename__ = "chronicle_events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    event_type = Column(String(50), nullable=False) # ACTIVITY_COMPLETED, LEVEL_UP, EVOLUTION_OCCURRED, STREAK_MILESTONE, ACHIEVEMENT_UNLOCKED, QUEST_CHAIN_COMPLETED
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    metadata_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)

    user = relationship("User", back_populates="chronicle_events")
