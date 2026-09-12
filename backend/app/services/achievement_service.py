from datetime import datetime, timezone
from typing import List
from sqlalchemy.orm import Session
from app.models.achievement import Achievement, UserAchievement
from app.schemas.activity import AchievementUnlocked

class AchievementService:
    @staticmethod
    def check_and_award(
        db: Session,
        user_id: int,
        code: str
    ) -> List[AchievementUnlocked]:
        unlocked = []
        
        # Check if achievement exists
        achievement = db.query(Achievement).filter(Achievement.code == code).first()
        if not achievement:
            return unlocked

        # Check if already unlocked
        existing = db.query(UserAchievement).filter(
            UserAchievement.user_id == user_id,
            UserAchievement.achievement_id == achievement.id
        ).first()

        if not existing:
            user_ach = UserAchievement(
                user_id=user_id,
                achievement_id=achievement.id,
                unlocked_at=datetime.now(timezone.utc)
            )
            db.add(user_ach)
            unlocked.append(AchievementUnlocked(
                code=achievement.code,
                name=achievement.name,
                description=achievement.description,
                icon_url=achievement.icon_url
            ))

        return unlocked
