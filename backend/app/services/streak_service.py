from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from app.models.streak import Streak

class StreakService:
    @staticmethod
    def get_user_current_date(tz_name: str = "UTC") -> date:
        try:
            tz = ZoneInfo(tz_name)
            return datetime.now(tz).date()
        except Exception:
            return datetime.now(timezone.utc).date()

    @staticmethod
    def update_streak(streak: Streak, tz_name: str = "UTC") -> bool:
        today = StreakService.get_user_current_date(tz_name)
        
        if streak.last_activity_date is None:
            # First activity ever
            streak.current_streak = 1
            streak.longest_streak = max(streak.longest_streak, 1)
            streak.last_activity_date = today
            return True

        if streak.last_activity_date == today:
            # Already completed an activity today; maintain current streak
            return False

        yesterday = today - timedelta(days=1)
        if streak.last_activity_date == yesterday:
            # Consecutive day! Increment streak
            streak.current_streak += 1
            streak.longest_streak = max(streak.longest_streak, streak.current_streak)
            streak.last_activity_date = today
            return True
        else:
            # Missed at least one day; reset streak to 1
            streak.current_streak = 1
            streak.longest_streak = max(streak.longest_streak, 1)
            streak.last_activity_date = today
            return True
