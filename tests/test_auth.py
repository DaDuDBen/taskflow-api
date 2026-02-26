def test_user_registration(client):
    payload = {"username": "alice", "password": "password123"}

    response = client.post("/register", json=payload)

    assert response.status_code == 200
    assert response.json() == {"message": "User created successfully"}


def test_login_returns_jwt_token(client):
    client.post("/register", json={"username": "bob", "password": "password123"})

    response = client.post(
        "/login",
        data={"username": "bob", "password": "password123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    body = response.json()
    assert response.status_code == 200
    assert "access_token" in body
    assert body["token_type"] == "bearer"
