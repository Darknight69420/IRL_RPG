from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.models.achievement import Achievement, UserAchievement
from app.schemas.achievement import AchievementResponse
from app.api.deps import get_current_user

router = APIRouter()

@router.get("", response_model=List[AchievementResponse])
def get_achievements(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    all_achievements = db.query(Achievement).all()
    user_unlocked = {
        ua.achievement_id: ua.unlocked_at for ua in db.query(UserAchievement).filter(
            UserAchievement.user_id == current_user.id
        ).all()
    }

    result = []
    for a in all_achievements:
        is_unlocked = a.id in user_unlocked
        unlocked_at = user_unlocked.get(a.id)
        result.append(AchievementResponse(
            id=a.id,
            code=a.code,
            name=a.name,
            description=a.description,
            icon_url=a.icon_url,
            is_unlocked=is_unlocked,
            unlocked_at=unlocked_at
        ))
    return result
