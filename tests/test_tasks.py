def test_create_task_authenticated(client):
    client.post(
        "/register",
        json={"username": "charlie", "password": "strongpass123"},
    )
    login_response = client.post(
        "/login",
        data={"username": "charlie", "password": "strongpass123"},
    )
    token = login_response.json()["access_token"]

    create_response = client.post(
        "/tasks",
        json={"title": "Write tests", "description": "Add FastAPI unit tests"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert create_response.status_code == 200
    assert create_response.json()["title"] == "Write tests"
    assert create_response.json()["description"] == "Add FastAPI unit tests"
    assert "id" in create_response.json()
