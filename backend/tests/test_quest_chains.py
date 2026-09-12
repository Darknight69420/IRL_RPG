def test_quest_chain_lifecycle_and_step_locking(client, auth_headers):
    # 1. Create a 2-step Goal Quest Chain
    create_res = client.post("/api/v1/quest-chains", headers=auth_headers, json={
        "title": "Launch Developer Portfolio",
        "description": "Build and showcase my projects",
        "steps": [
            {
                "step_order": 1,
                "title": "Design Wireframes in Figma",
                "difficulty": "EASY",
                "primary_attribute": "INT"
            },
            {
                "step_order": 2,
                "title": "Deploy to Vercel",
                "difficulty": "MEDIUM",
                "primary_attribute": "DIS"
            }
        ]
    })
    assert create_res.status_code == 201
    chain = create_res.json()
    chain_id = chain["id"]
    step1_id = chain["steps"][0]["id"]
    step2_id = chain["steps"][1]["id"]

    assert chain["steps"][0]["status"] == "UNLOCKED"
    assert chain["steps"][1]["status"] == "LOCKED"

    # 2. Try to complete Step 2 before Step 1 -> Should be rejected
    bad_step = client.post(f"/api/v1/quest-chains/{chain_id}/steps/{step2_id}/complete", headers=auth_headers)
    assert bad_step.status_code == 400
    assert bad_step.json()["detail"]["error_code"] == "LOCKED_STEP"

    # 3. Complete Step 1 -> Step 2 should now unlock
    step1_res = client.post(f"/api/v1/quest-chains/{chain_id}/steps/{step1_id}/complete", headers=auth_headers)
    assert step1_res.status_code == 200
    assert step1_res.json()["step_status"] == "COMPLETED"
    assert step1_res.json()["chain_completed"] == False

    # Verify Step 2 is now UNLOCKED
    get_chain = client.get(f"/api/v1/quest-chains/{chain_id}", headers=auth_headers)
    assert get_chain.json()["steps"][1]["status"] == "UNLOCKED"

    # 4. Complete Step 2 -> Chain should be completed with bonus XP!
    step2_res = client.post(f"/api/v1/quest-chains/{chain_id}/steps/{step2_id}/complete", headers=auth_headers)
    assert step2_res.status_code == 200
    data = step2_res.json()
    assert data["chain_completed"] == True
    assert data["bonus_xp"] > 0
    ach_codes = [a["code"] for a in data["new_achievements"]]
    assert "CHAIN_COMPLETED" in ach_codes
