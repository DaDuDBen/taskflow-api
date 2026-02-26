def test_user_registration(client):
    response = client.post(
        "/register",
        json={"username": "alice", "password": "strongpass123"},
    )

    assert response.status_code == 200
    assert response.json() == {"message": "User created successfully"}


def test_login_generates_jwt_token(client):
    client.post(
        "/register",
        json={"username": "bob", "password": "strongpass123"},
    )

    response = client.post(
        "/login",
        data={"username": "bob", "password": "strongpass123"},
    )

    body = response.json()

    assert response.status_code == 200
    assert body["token_type"] == "bearer"
    assert body["access_token"]
