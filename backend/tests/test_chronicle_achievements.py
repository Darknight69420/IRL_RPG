def test_chronicle_pagination(client, auth_headers):
    # Perform an action to create chronicle events
    act = client.post("/api/v1/activities", headers=auth_headers, json={
        "title": "Evening Walk",
        "category": "TASK",
        "difficulty": "EASY",
        "primary_attribute": "VIT"
    }).json()
    client.post(f"/api/v1/activities/{act['id']}/complete", headers=auth_headers)

    # Fetch page 1
    res = client.get("/api/v1/chronicle?page=1&page_size=10", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["total"] >= 1
    assert len(data["items"]) >= 1
    assert data["page"] == 1
    assert data["page_size"] == 10

def test_achievements_listing_and_unlock_status(client, auth_headers):
    # Get all achievements
    res = client.get("/api/v1/achievements", headers=auth_headers)
    assert res.status_code == 200
    achievements = res.json()
    assert len(achievements) >= 5
    
    # Complete an activity to ensure FIRST_STEP is unlocked
    act = client.post("/api/v1/activities", headers=auth_headers, json={
        "title": "Read Architecture Chapter",
        "category": "TASK",
        "difficulty": "MEDIUM",
        "primary_attribute": "INT"
    }).json()
    client.post(f"/api/v1/activities/{act['id']}/complete", headers=auth_headers)

    res2 = client.get("/api/v1/achievements", headers=auth_headers)
    assert res2.status_code == 200
    ach_map = {a["code"]: a for a in res2.json()}
    assert ach_map["FIRST_STEP"]["is_unlocked"] == True
    assert ach_map["FIRST_STEP"]["unlocked_at"] is not None
