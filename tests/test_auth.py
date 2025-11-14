def test_register_creates_user_and_token(client):
    resp = client.post(
        "/auth/register",
        json={
            "name": "Rhoda",
            "email": "rhoda@example.com",
            "password": "secret",
            "is_agent": False,
        },
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert "access_token" in data
    assert data["user"]["email"] == "rhoda@example.com"


def test_register_duplicate_email_fails(client):
    payload = {
        "name": "User",
        "email": "dup@example.com",
        "password": "secret",
    }

    r1 = client.post("/auth/register", json=payload)
    assert r1.status_code == 201

    r2 = client.post("/auth/register", json=payload)
    assert r2.status_code == 400
    data = r2.get_json()
    assert "Email already registered" in data["message"]


def test_login_success(client):
    # first register
    client.post(
        "/auth/register",
        json={
            "name": "Login User",
            "email": "login@example.com",
            "password": "secret",
        },
    )

    resp = client.post(
        "/auth/login",
        json={"email": "login@example.com", "password": "secret"},
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert "access_token" in data
    assert data["user"]["email"] == "login@example.com"


def test_login_invalid_credentials(client):
    resp = client.post(
        "/auth/login",
        json={"email": "nope@example.com", "password": "wrong"},
    )
    assert resp.status_code == 401
    data = resp.get_json()
    assert "Invalid credentials" in data["message"]
