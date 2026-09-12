from datetime import datetime, timezone
from typing import List, Tuple
from sqlalchemy.orm import Session
from app.models.quest_chain import QuestChain, QuestStep
from app.core.exceptions import LockedQuestStepException, GameRuleException

class QuestService:
    @staticmethod
    def create_chain(db: Session, user_id: int, title: str, description: str, steps_data: list) -> QuestChain:
        chain = QuestChain(
            user_id=user_id,
            title=title,
            description=description,
            status="IN_PROGRESS"
        )
        db.add(chain)
        db.flush()

        for idx, s in enumerate(steps_data):
            step_order = s.get("step_order", idx + 1)
            # First step is UNLOCKED; subsequent are LOCKED
            status = "UNLOCKED" if step_order == 1 else "LOCKED"
            step = QuestStep(
                chain_id=chain.id,
                step_order=step_order,
                title=s.get("title"),
                difficulty=s.get("difficulty", "MEDIUM"),
                primary_attribute=s.get("primary_attribute", "INT"),
                status=status
            )
            db.add(step)
            
        db.commit()
        db.refresh(chain)
        return chain

    @staticmethod
    def validate_and_complete_step(db: Session, chain: QuestChain, step: QuestStep) -> Tuple[bool, bool]:
        if step.status == "COMPLETED":
            raise GameRuleException("STEP_ALREADY_COMPLETED", "This quest step is already marked complete.")

        # Check prerequisite
        if step.step_order > 1:
            prev_step = db.query(QuestStep).filter(
                QuestStep.chain_id == chain.id,
                QuestStep.step_order == step.step_order - 1
            ).first()
            if not prev_step or prev_step.status != "COMPLETED":
                raise LockedQuestStepException(required_step_order=step.step_order - 1)

        # Mark step complete
        step.status = "COMPLETED"
        step.completed_at = datetime.now(timezone.utc)
        db.flush()

        # Unlock next step if exists
        next_step = db.query(QuestStep).filter(
            QuestStep.chain_id == chain.id,
            QuestStep.step_order == step.step_order + 1
        ).first()
        if next_step and next_step.status == "LOCKED":
            next_step.status = "UNLOCKED"
            db.flush()

        # Check if entire chain is complete
        total_remaining = db.query(QuestStep).filter(
            QuestStep.chain_id == chain.id,
            QuestStep.status != "COMPLETED"
        ).count()

        chain_completed = (total_remaining == 0)
        if chain_completed:
            chain.status = "COMPLETED"
            chain.completed_at = datetime.now(timezone.utc)
            db.flush()

        return True, chain_completed
