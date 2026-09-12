from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.services.progression_engine import ProgressionEngine
from app.services.attribute_service import AttributeService
from app.schemas.character import CharacterResponse, AttributesResponse, StreakInfo
from app.api.deps import get_current_user

router = APIRouter()

@router.get("", response_model=CharacterResponse)
def get_character(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    character = current_user.character
    streak = current_user.streak
    
    attr_map = {a.code: a.value for a in character.attributes} if character.attributes else {}
    for code in ["STR", "INT", "WIS", "DIS", "VIT", "CHA"]:
        attr_map.setdefault(code, 0.0)

    xp_next = ProgressionEngine.cumulative_xp_for_level(character.level + 1)

    return CharacterResponse(
        id=character.id,
        user_id=current_user.id,
        level=character.level,
        current_xp=character.current_xp,
        xp_for_next_level=xp_next,
        streak=StreakInfo(
            current_streak=streak.current_streak if streak else 0,
            longest_streak=streak.longest_streak if streak else 0,
            last_activity_date=streak.last_activity_date if streak else None
        ),
        attributes=attr_map
    )

@router.get("/attributes", response_model=AttributesResponse)
def get_attributes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    character = current_user.character
    attr_map = {a.code: a.value for a in character.attributes} if character.attributes else {}
    for code in ["STR", "INT", "WIS", "DIS", "VIT", "CHA"]:
        attr_map.setdefault(code, 0.0)

    dominant_attr, max_pct, percentages = AttributeService.calculate_dominance(attr_map)

    return AttributesResponse(
        attributes=attr_map,
        dominant_attribute=dominant_attr,
        attribute_percentages=percentages
    )
