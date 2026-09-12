from app.services.progression_engine import ProgressionEngine

def test_deterministic_evolution_to_luminaur(client, auth_headers):
    # Setup high INT activity
    act_res = client.post("/api/v1/activities", headers=auth_headers, json={
        "title": "Deep Architecture Study",
        "category": "TASK",
        "difficulty": "HEROIC", # 140 XP, 25 INT points
        "primary_attribute": "INT"
    })
    act_id = act_res.json()["id"]

    # Level 10 requires 3,365 XP.
    # We will complete the heroic task multiple times to cross 3,400 XP and bond 40+
    evolution_diff = None
    for i in range(26):
        res = client.post(f"/api/v1/activities/{act_id}/complete", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        if data["creature"]["evolution_triggered"]:
            evolution_diff = data
            break

    assert evolution_diff is not None, "Evolution was not triggered after sufficient XP and bond!"
    assert evolution_diff["creature"]["evolved_from"] == "Aetherling"
    assert evolution_diff["creature"]["evolved_to"] == "Luminaur"
    assert evolution_diff["creature"]["species_code"] == "LUMINAUR"
    assert evolution_diff["creature"]["evolution_tier"] == 2

    # Check that FIRST_EVOLUTION achievement was awarded
    ach_codes = [a["code"] for a in evolution_diff["new_achievements"]]
    assert "FIRST_EVOLUTION" in ach_codes

    # Check Lifedex collection
    col_res = client.get("/api/v1/creatures/collection", headers=auth_headers)
    assert col_res.status_code == 200
    col_items = {item["species_code"]: item for item in col_res.json()}
    assert col_items["AETHERLING"]["status"] == "AWAKENED"
    assert col_items["LUMINAUR"]["status"] == "AWAKENED"
    assert col_items["PYROKYN"]["status"] == "LOCKED"

    # Test switching active companion back to Aetherling
    aetherling_id = col_items["AETHERLING"]["species_id"]
    switch_res = client.post(f"/api/v1/creatures/active/{aetherling_id}", headers=auth_headers)
    assert switch_res.status_code == 200
    assert switch_res.json()["species"]["code"] == "AETHERLING"

def test_evolution_locked_species_switch_prevented(client, auth_headers):
    # Attempting to activate locked Pyrokyn
    col_res = client.get("/api/v1/creatures/collection", headers=auth_headers)
    pyrokyn_id = next(item["species_id"] for item in col_res.json() if item["species_code"] == "PYROKYN")
    
    switch_res = client.post(f"/api/v1/creatures/active/{pyrokyn_id}", headers=auth_headers)
    assert switch_res.status_code == 400
    assert switch_res.json()["detail"]["error_code"] == "FORM_NOT_UNLOCKED"

def test_deterministic_evolution_to_pyrokyn(client, second_auth_headers):
    # Setup high STR activity
    act_res = client.post("/api/v1/activities", headers=second_auth_headers, json={
        "title": "Heavy Deadlifts & Sprints",
        "category": "TASK",
        "difficulty": "HEROIC",
        "primary_attribute": "STR"
    })
    act_id = act_res.json()["id"]

    evolution_diff = None
    for i in range(26):
        res = client.post(f"/api/v1/activities/{act_id}/complete", headers=second_auth_headers)
        assert res.status_code == 200
        data = res.json()
        if data["creature"]["evolution_triggered"]:
            evolution_diff = data
            break

    assert evolution_diff is not None
    assert evolution_diff["creature"]["evolved_to"] == "Pyrokyn"
    assert evolution_diff["creature"]["species_code"] == "PYROKYN"
    assert evolution_diff["creature"]["evolution_tier"] == 2

def test_deterministic_evolution_to_harmonix(client):
    # Register fresh user
    reg = client.post("/api/v1/auth/register", json={
        "username": "polymath_hero",
        "email": "polymath@test.com",
        "password": "Password123!"
    }).json()
    headers = {"Authorization": f"Bearer {reg['access_token']}"}

    # Create 6 balanced activities for each attribute
    attrs = ["STR", "INT", "WIS", "DIS", "VIT", "CHA"]
    act_ids = []
    for a in attrs:
        created = client.post("/api/v1/activities", headers=headers, json={
            "title": f"Practice {a}",
            "category": "TASK",
            "difficulty": "MEDIUM",
            "primary_attribute": a
        }).json()
        act_ids.append(created["id"])

    # Rotate through all 6 evenly until Level 10 is reached
    evolution_diff = None
    for loop in range(12): # 12 * 6 = 72 activities, ~3600 XP
        for aid in act_ids:
            res = client.post(f"/api/v1/activities/{aid}/complete", headers=headers)
            assert res.status_code == 200
            data = res.json()
            if data["creature"]["evolution_triggered"]:
                evolution_diff = data
                break
        if evolution_diff:
            break

    assert evolution_diff is not None, "Harmonix evolution was not triggered!"
    assert evolution_diff["creature"]["evolved_to"] == "Harmonix"
    assert evolution_diff["creature"]["species_code"] == "HARMONIX"
    assert evolution_diff["creature"]["evolution_tier"] == 2

