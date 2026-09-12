def test_activity_completion_and_progression_diff(client, auth_headers):
    # Create an activity
    create_res = client.post("/api/v1/activities", headers=auth_headers, json={
        "title": "Morning 5km Run",
        "category": "TASK", # Use TASK so we can test repeatable completion without daily cooldown
        "difficulty": "MEDIUM", # 50 XP, 8 Attribute points
        "primary_attribute": "STR",
        "secondary_attribute": "VIT"
    })
    act_id = create_res.json()["id"]

    # Complete activity
    comp_res = client.post(f"/api/v1/activities/{act_id}/complete", headers=auth_headers, json={
        "notes": "Felt fast, heart rate 145 bpm"
    })
    assert comp_res.status_code == 200
    data = comp_res.json()

    # Verify Progression Diff
    assert data["activity_id"] == act_id
    assert data["xp_earned"] == 51 # 20 * 2.5 * (1 + 0.02 streak bonus)
    # Primary (STR): ceil(8 * 0.70) = 6.0; Secondary (VIT): floor(8 * 0.30) = 2.0
    assert data["attribute_gains"]["STR"] == 6.0
    assert data["attribute_gains"]["VIT"] == 2.0

    # Character progression check
    assert data["character"]["current_xp"] == 51
    assert data["character"]["level"] == 1

    # Creature progression check
    assert data["creature"]["name"] is not None
    assert data["creature"]["current_level"] >= 1
    assert data["creature"]["bond_score"] > 10

    # First Step achievement should be awarded
    ach_codes = [a["code"] for a in data["new_achievements"]]
    assert "FIRST_STEP" in ach_codes

    # Verify Chronicle has the recorded entry
    chron_res = client.get("/api/v1/chronicle", headers=auth_headers)
    assert chron_res.status_code == 200
    events = chron_res.json()["items"]
    assert any(e["event_type"] == "ACTIVITY_COMPLETED" for e in events)
