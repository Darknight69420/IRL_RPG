def test_register_and_login_flow(client):
    # 1. Register new user
    reg_res = client.post("/api/v1/auth/register", json={
        "username": "arcane_scholar",
        "email": "scholar@example.com",
        "password": "SecurePassword999!",
        "timezone": "UTC"
    })
    assert reg_res.status_code == 201
    data = reg_res.json()
    assert "access_token" in data
    assert data["user"]["username"] == "arcane_scholar"
    token = data["access_token"]

    # 2. Re-registration with same username should fail
    dup_res = client.post("/api/v1/auth/register", json={
        "username": "arcane_scholar",
        "email": "different@example.com",
        "password": "SecurePassword999!"
    })
    assert dup_res.status_code == 400
    assert dup_res.json()["detail"]["error_code"] == "USERNAME_TAKEN"

    # 3. Login with valid credentials
    login_res = client.post("/api/v1/auth/login", json={
        "username": "arcane_scholar",
        "password": "SecurePassword999!"
    })
    assert login_res.status_code == 200
    assert "access_token" in login_res.json()

    # 4. Login with invalid password
    bad_login = client.post("/api/v1/auth/login", json={
        "username": "arcane_scholar",
        "password": "WrongPassword!"
    })
    assert bad_login.status_code == 401
    assert bad_login.json()["detail"]["error_code"] == "INVALID_CREDENTIALS"

    # 5. Access /auth/me with Bearer token
    me_res = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_res.status_code == 200
    assert me_res.json()["username"] == "arcane_scholar"

def test_unauthenticated_access_rejected(client):
    res = client.get("/api/v1/auth/me")
    assert res.status_code == 403 or res.status_code == 401
