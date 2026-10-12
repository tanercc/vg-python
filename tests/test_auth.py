def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "Test12345!",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == "test@example.com"
    assert data["is_admin"] is False

    assert "password" not in data
    assert "password_hash" not in data


def test_duplicate_email_returns_409(client):
    payload = {
        "email": "duplicate@example.com",
        "password": "Test12345!",
    }

    first_response = client.post(
        "/auth/register",
        json=payload,
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/auth/register",
        json=payload,
    )

    assert second_response.status_code == 409

    assert second_response.json() == {
        "detail": "Email already registered"
    }    


def test_invalid_email_returns_422(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "wrong-email",
            "password": "Test12345!",
        },
    )

    assert response.status_code == 422   


def test_short_password_returns_422(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "123",
        },
    )

    assert response.status_code == 422    


def test_login_returns_access_token(client):
    client.post(
        "/auth/register",
        json={
            "email": "login@example.com",
            "password": "Test12345!",
        },
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "login@example.com",
            "password": "Test12345!",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"     


def test_wrong_password_returns_401(client):
    client.post(
        "/auth/register",
        json={
            "email": "wrong@example.com",
            "password": "Test12345!",
        },
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "wrong@example.com",
            "password": "WrongPassword!",
        },
    )

    assert response.status_code == 401

    assert response.json() == {
        "detail": "Invalid credentials"
    }    


def test_me_returns_current_user(
    client,
    auth_headers,
):
    response = client.get(
        "/auth/me",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["email"]
        == "authenticated@example.com"
    )    