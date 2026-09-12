from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base

class QuestChain(Base):
    __tablename__ = "quest_chains"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), default="IN_PROGRESS", nullable=False) # IN_PROGRESS, COMPLETED, ABANDONED
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="quest_chains")
    steps = relationship("QuestStep", back_populates="chain", order_by="QuestStep.step_order", cascade="all, delete-orphan")

class QuestStep(Base):
    __tablename__ = "quest_steps"

    id = Column(Integer, primary_key=True, index=True)
    chain_id = Column(Integer, ForeignKey("quest_chains.id", ondelete="CASCADE"), nullable=False, index=True)
    step_order = Column(Integer, nullable=False)
    title = Column(String(200), nullable=False)
    difficulty = Column(String(20), default="MEDIUM", nullable=False) # TRIVIAL, EASY, MEDIUM, HARD, HEROIC
    primary_attribute = Column(String(10), default="INT", nullable=False)
    status = Column(String(20), default="LOCKED", nullable=False) # LOCKED, UNLOCKED, COMPLETED
    completed_at = Column(DateTime, nullable=True)

    __table_args__ = (
        UniqueConstraint("chain_id", "step_order", name="uq_chain_step_order"),
    )

    chain = relationship("QuestChain", back_populates="steps")
