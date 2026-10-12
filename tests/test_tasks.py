def test_create_task(
    client,
    auth_headers,
):
    response = client.post(
        "/tasks",
        headers=auth_headers,
        json={
            "title": "Test task",
            "description": "Study FastAPI",
            "status": "pending",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Test task"
    assert data["status"] == "pending"
    assert "user_id" in data


def test_create_task_without_login_returns_401(
    client,
):
    response = client.post(
        "/tasks",
        json={
            "title": "Private task",
            "status": "pending",
        },
    )

    assert response.status_code == 401


def test_user_sees_own_tasks(
    client,
    auth_headers,
):
    client.post(
        "/tasks",
        headers=auth_headers,
        json={
            "title": "Task 1",
            "status": "pending",
        },
    )

    client.post(
        "/tasks",
        headers=auth_headers,
        json={
            "title": "Task 2",
            "status": "completed",
        },
    )

    response = client.get(
        "/tasks",
        headers=auth_headers,
    )

    assert response.status_code == 200

    tasks = response.json()

    assert len(tasks) == 2


def test_user_cannot_access_another_users_task(
    client,
):
    client.post(
        "/auth/register",
        json={
            "email": "user1@example.com",
            "password": "Test12345!",
        },
    )

    login_1 = client.post(
        "/auth/login",
        data={
            "username": "user1@example.com",
            "password": "Test12345!",
        },
    )

    token_1 = login_1.json()["access_token"]

    headers_1 = {
        "Authorization": f"Bearer {token_1}"
    }

    task_response = client.post(
        "/tasks",
        headers=headers_1,
        json={
            "title": "User 1 private task",
            "status": "pending",
        },
    )

    task_id = task_response.json()["id"]

    client.post(
        "/auth/register",
        json={
            "email": "user2@example.com",
            "password": "Test12345!",
        },
    )

    login_2 = client.post(
        "/auth/login",
        data={
            "username": "user2@example.com",
            "password": "Test12345!",
        },
    )

    token_2 = login_2.json()["access_token"]

    headers_2 = {
        "Authorization": f"Bearer {token_2}"
    }

    response = client.get(
        f"/tasks/{task_id}",
        headers=headers_2,
    )

    assert response.status_code == 403


def test_update_task(
    client,
    auth_headers,
):
    create_response = client.post(
        "/tasks",
        headers=auth_headers,
        json={
            "title": "Old title",
            "status": "pending",
        },
    )

    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        headers=auth_headers,
        json={
            "title": "New title",
            "status": "completed",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "New title"
    assert data["status"] == "completed"


def test_delete_task(
    client,
    auth_headers,
):
    create_response = client.post(
        "/tasks",
        headers=auth_headers,
        json={
            "title": "Delete me",
            "status": "pending",
        },
    )

    task_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/tasks/{task_id}",
        headers=auth_headers,
    )

    assert delete_response.status_code == 204

    get_response = client.get(
        f"/tasks/{task_id}",
        headers=auth_headers,
    )

    assert get_response.status_code == 404


