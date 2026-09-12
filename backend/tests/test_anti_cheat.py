def test_habit_cooldown_enforcement(client, auth_headers):
    # 1. Create a daily HABIT
    act_res = client.post("/api/v1/activities", headers=auth_headers, json={
        "title": "Drink 2L Water",
        "category": "HABIT",
        "difficulty": "TRIVIAL",
        "primary_attribute": "VIT",
        "cooldown_hours": 24
    })
    act_id = act_res.json()["id"]

    # 2. Complete for the first time today -> Success
    res1 = client.post(f"/api/v1/activities/{act_id}/complete", headers=auth_headers)
    assert res1.status_code == 200

    # 3. Complete again on the same day -> Rejection with 409 COOLDOWN_ACTIVE
    res2 = client.post(f"/api/v1/activities/{act_id}/complete", headers=auth_headers)
    assert res2.status_code == 409
    assert res2.json()["detail"]["error_code"] == "COOLDOWN_ACTIVE"

def test_cross_user_isolation(client, auth_headers, second_auth_headers):
    # User 1 creates an activity
    u1_act = client.post("/api/v1/activities", headers=auth_headers, json={
        "title": "User 1 Private Habit",
        "category": "TASK",
        "difficulty": "MEDIUM",
        "primary_attribute": "INT"
    }).json()
    u1_act_id = u1_act["id"]

    # User 2 tries to read User 1's activity -> 403 Forbidden
    read_res = client.get(f"/api/v1/activities/{u1_act_id}", headers=second_auth_headers)
    assert read_res.status_code == 403
    assert read_res.json()["detail"]["error_code"] == "FORBIDDEN"

    # User 2 tries to complete User 1's activity -> 403 Forbidden
    comp_res = client.post(f"/api/v1/activities/{u1_act_id}/complete", headers=second_auth_headers)
    assert comp_res.status_code == 403
    assert comp_res.json()["detail"]["error_code"] == "FORBIDDEN"

    # User 2 tries to delete User 1's activity -> 403 Forbidden
    del_res = client.delete(f"/api/v1/activities/{u1_act_id}", headers=second_auth_headers)
    assert del_res.status_code == 403
    assert del_res.json()["detail"]["error_code"] == "FORBIDDEN"

def test_inactive_activity_completion_blocked(client, auth_headers):
    # Create inactive activity
    act = client.post("/api/v1/activities", headers=auth_headers, json={
        "title": "Old Archived Habit",
        "category": "TASK",
        "difficulty": "EASY",
        "primary_attribute": "WIS"
    }).json()
    act_id = act["id"]

    # Deactivate it
    client.patch(f"/api/v1/activities/{act_id}", headers=auth_headers, json={"is_active": False})

    # Try to complete
    res = client.post(f"/api/v1/activities/{act_id}/complete", headers=auth_headers)
    assert res.status_code == 400
    assert res.json()["detail"]["error_code"] == "ACTIVITY_INACTIVE"
