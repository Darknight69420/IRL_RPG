def test_activity_crud(client, auth_headers):
    # 1. Create habit
    create_res = client.post("/api/v1/activities", headers=auth_headers, json={
        "title": "Solve 2 LeetCode problems",
        "description": "Dynamic programming practice",
        "category": "HABIT",
        "difficulty": "HARD",
        "primary_attribute": "INT",
        "secondary_attribute": "DIS",
        "cooldown_hours": 24
    })
    assert create_res.status_code == 201
    act_data = create_res.json()
    assert act_data["title"] == "Solve 2 LeetCode problems"
    assert act_data["primary_attribute"] == "INT"
    assert act_data["secondary_attribute"] == "DIS"
    act_id = act_data["id"]

    # 2. Get list of activities
    list_res = client.get("/api/v1/activities", headers=auth_headers)
    assert list_res.status_code == 200
    assert len(list_res.json()) >= 1

    # 3. Patch activity
    patch_res = client.patch(f"/api/v1/activities/{act_id}", headers=auth_headers, json={
        "title": "Solve 3 LeetCode problems",
        "difficulty": "HEROIC"
    })
    assert patch_res.status_code == 200
    assert patch_res.json()["title"] == "Solve 3 LeetCode problems"
    assert patch_res.json()["difficulty"] == "HEROIC"

    # 4. Delete activity
    del_res = client.delete(f"/api/v1/activities/{act_id}", headers=auth_headers)
    assert del_res.status_code == 204

    # 5. Confirm deleted
    get_res = client.get(f"/api/v1/activities/{act_id}", headers=auth_headers)
    assert get_res.status_code == 404
