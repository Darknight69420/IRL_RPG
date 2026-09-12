from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.models.quest_chain import QuestChain, QuestStep
from app.core.exceptions import ResourceNotFoundException, UnauthorizedResourceAccessException
from app.schemas.quest_chain import (
    QuestChainCreate, QuestChainResponse, QuestStepResponse
)
from app.schemas.activity import ActivityCompletionResponse, CharacterProgressionDiff, CreatureProgressionDiff, StreakDiff
from app.services.quest_service import QuestService
from app.services.progression_engine import ProgressionEngine
from app.services.creature_service import CreatureService
from app.services.attribute_service import AttributeService
from app.services.chronicle_service import ChronicleService
from app.services.achievement_service import AchievementService
from app.api.deps import get_current_user

router = APIRouter()

def _to_chain_response(chain: QuestChain) -> QuestChainResponse:
    total_steps = len(chain.steps)
    completed_steps = sum(1 for s in chain.steps if s.status == "COMPLETED")
    return QuestChainResponse(
        id=chain.id,
        user_id=chain.user_id,
        title=chain.title,
        description=chain.description,
        status=chain.status,
        total_steps=total_steps,
        completed_steps=completed_steps,
        steps=[QuestStepResponse.model_validate(s) for s in chain.steps],
        created_at=chain.created_at,
        completed_at=chain.completed_at
    )

@router.get("", response_model=List[QuestChainResponse])
def get_quest_chains(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chains = db.query(QuestChain).filter(
        QuestChain.user_id == current_user.id
    ).order_by(QuestChain.created_at.desc()).all()
    return [_to_chain_response(c) for c in chains]

@router.post("", response_model=QuestChainResponse, status_code=status.HTTP_201_CREATED)
def create_quest_chain(
    chain_in: QuestChainCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    steps_data = [s.model_dump() for s in chain_in.steps]
    chain = QuestService.create_chain(
        db=db,
        user_id=current_user.id,
        title=chain_in.title,
        description=chain_in.description or "",
        steps_data=steps_data
    )
    return _to_chain_response(chain)

@router.get("/{chain_id}", response_model=QuestChainResponse)
def get_quest_chain(
    chain_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chain = db.query(QuestChain).filter(QuestChain.id == chain_id).first()
    if not chain:
        raise ResourceNotFoundException("QuestChain", chain_id)
    if chain.user_id != current_user.id:
        raise UnauthorizedResourceAccessException()
    return _to_chain_response(chain)

@router.post("/{chain_id}/steps/{step_id}/complete")
def complete_quest_step(
    chain_id: int,
    step_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chain = db.query(QuestChain).filter(QuestChain.id == chain_id).first()
    if not chain:
        raise ResourceNotFoundException("QuestChain", chain_id)
    if chain.user_id != current_user.id:
        raise UnauthorizedResourceAccessException()

    step = db.query(QuestStep).filter(
        QuestStep.id == step_id,
        QuestStep.chain_id == chain_id
    ).first()
    if not step:
        raise ResourceNotFoundException("QuestStep", step_id)

    # Validate prerequisite & complete step
    _, chain_completed = QuestService.validate_and_complete_step(db, chain, step)

    # Award step progression
    character = current_user.character
    streak = current_user.streak
    creature = current_user.creatures[0] if current_user.creatures else None

    xp_earned, _ = ProgressionEngine.calculate_xp_earned(step.difficulty, streak.current_streak if streak else 0)
    
    # Chain completion bonus: +50% XP and +25 Bond!
    bonus_xp = int(xp_earned * 0.50) if chain_completed else 0
    total_xp = xp_earned + bonus_xp

    character.current_xp += total_xp
    new_char_level, _, _ = ProgressionEngine.calculate_level_from_xp(character.current_xp)
    character.level = new_char_level

    # Attribute gains
    gains = AttributeService.calculate_gains(step.difficulty, step.primary_attribute)
    char_attrs = {ca.code: ca for ca in character.attributes}
    for code, gain in gains.items():
        if code in char_attrs:
            char_attrs[code].value += gain

    # Creature bond
    if creature:
        creature.current_xp += total_xp
        new_creature_level, _, _ = ProgressionEngine.calculate_level_from_xp(creature.current_xp)
        creature.level = new_creature_level
        CreatureService.award_bond(creature, 5)
        if chain_completed:
            CreatureService.award_bond(creature, 25)

    # Chronicle event
    ChronicleService.record_event(
        db=db,
        user_id=current_user.id,
        event_type="QUEST_STEP_COMPLETED",
        title=f"Step Completed: {step.title}",
        description=f"Part of '{chain.title}'. Earned {total_xp} XP.",
        metadata={"chain_id": chain.id, "step_id": step.id, "chain_completed": chain_completed}
    )

    new_achievements = []
    if chain_completed:
        ChronicleService.record_event(
            db=db,
            user_id=current_user.id,
            event_type="QUEST_CHAIN_COMPLETED",
            title=f"Goal Achieved: {chain.title}!",
            description="All milestone steps successfully conquered.",
            metadata={"chain_id": chain.id}
        )
        new_achievements.extend(AchievementService.check_and_award(db, current_user.id, "CHAIN_COMPLETED"))

    db.commit()
    db.refresh(chain)

    return {
        "step_id": step.id,
        "step_status": step.status,
        "chain_id": chain.id,
        "chain_status": chain.status,
        "chain_completed": chain_completed,
        "xp_earned": total_xp,
        "bonus_xp": bonus_xp,
        "new_achievements": [a.model_dump() for a in new_achievements]
    }
