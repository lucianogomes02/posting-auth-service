from datetime import datetime, timedelta
from http import HTTPStatus

from freezegun import freeze_time


def test_get_token(client, user_test, engine):
    response = client.post(
        "/auth/login",
        data={"username": user_test.email, "password": "123456"},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert "access_token" in token
    assert "token_type" in token


def test_token_expired_after_time(client, user_test):
    with freeze_time(datetime.now()):
        response = client.post(
            "/auth/login",
            data={"username": user_test.email, "password": "123456"},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()["access_token"]

    with freeze_time(datetime.now() + timedelta(hours=1)):
        response = client.put(
            f"/user/{user_test.id}",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "username": "wrongwrong",
                "email": "wrong@wrong.com",
                "password": "wrong",
            },
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {"detail": "Could not validate credentials"}


def test_token_inexistent_user(client):
    response = client.post(
        "/auth/login",
        data={"username": "no_user@no_domain.com", "password": "testtest"},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Incorrect email or password"}


def test_token_wrong_password(client, user_test):
    response = client.post(
        "/auth/login",
        data={"username": user_test.email, "password": "wrong_password"},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Incorrect email or password"}


def test_refresh_token(client, user_test, token):
    response = client.post(
        "/auth/refresh_token",
        headers={"Authorization": f"Bearer {token}"},
    )

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"


def test_token_expired_dont_refresh(client, user_test):
    with freeze_time("2023-07-14 12:00:00"):
        response = client.post(
            "/auth/login",
            data={"username": user_test.email, "password": "123456"},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()["access_token"]

    with freeze_time("2023-07-14 12:31:00"):
        response = client.post(
            "/auth/refresh_token",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {"detail": "Could not validate credentials"}
