from datetime import date, timedelta
from app.services.streak_service import StreakService
from app.models.streak import Streak

def test_streak_progression_and_bonus(client, auth_headers):
    # 1. Create a task
    act_res = client.post("/api/v1/activities", headers=auth_headers, json={
        "title": "Daily Journaling",
        "category": "TASK",
        "difficulty": "EASY",
        "primary_attribute": "WIS"
    })
    act_id = act_res.json()["id"]

    # 2. First completion
    res1 = client.post(f"/api/v1/activities/{act_id}/complete", headers=auth_headers)
    assert res1.status_code == 200
    assert res1.json()["streak"]["current_streak"] == 1
    assert res1.json()["streak"]["streak_advanced"] == True

    # 3. Second completion on same day
    res2 = client.post(f"/api/v1/activities/{act_id}/complete", headers=auth_headers)
    assert res2.status_code == 200
    assert res2.json()["streak"]["current_streak"] == 1
    assert res2.json()["streak"]["streak_advanced"] == False

def test_streak_service_date_transitions():
    streak = Streak(user_id=1, current_streak=1, longest_streak=1)
    today = date.today()
    yesterday = today - timedelta(days=1)
    two_days_ago = today - timedelta(days=2)

    # 1. Activity yesterday -> should increment today
    streak.last_activity_date = yesterday
    advanced = StreakService.update_streak(streak, "UTC")
    assert advanced == True
    assert streak.current_streak == 2
    assert streak.longest_streak == 2

    # 2. Activity today again -> should maintain
    advanced2 = StreakService.update_streak(streak, "UTC")
    assert advanced2 == False
    assert streak.current_streak == 2

    # 3. Missed day (last active 2 days ago) -> reset to 1
    streak.last_activity_date = two_days_ago
    advanced3 = StreakService.update_streak(streak, "UTC")
    assert advanced3 == True
    assert streak.current_streak == 1
    assert streak.longest_streak == 2
