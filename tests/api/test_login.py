from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_login_success() -> None:
    response = client.post(
        "/login",
        json={"username": "admin", "password": "password123"},
    )

    assert response.status_code == 200
    assert response.json()["token"] == "demo-token"
    assert response.json()["username"] == "admin"


def test_login_fails_with_wrong_password() -> None:
    response = client.post(
        "/login",
        json={"username": "admin", "password": "wrong-password"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"


def test_login_requires_password() -> None:
    response = client.post("/login", json={"username": "admin"})

    assert response.status_code == 422
