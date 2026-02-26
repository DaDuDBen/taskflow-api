def test_create_task_authenticated(client):
    client.post("/register", json={"username": "charlie", "password": "password123"})
    login_response = client.post(
        "/login",
        data={"username": "charlie", "password": "password123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = login_response.json()["access_token"]

    response = client.post(
        "/tasks",
        json={"title": "Learn CI", "description": "Add GitHub Actions"},
        headers={"Authorization": f"Bearer {token}"},
    )

    body = response.json()
    assert response.status_code == 200
    assert body["title"] == "Learn CI"
    assert body["description"] == "Add GitHub Actions"
    assert "id" in body
