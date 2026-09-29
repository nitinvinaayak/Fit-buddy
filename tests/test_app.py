from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"


def test_home_page():
    response = client.get("/")

    assert response.status_code == 200
    assert "FitBuddy" in response.text


def test_admin_page_requires_key():
    response = client.get("/view-all-users")

    assert response.status_code == 401
    assert "Invalid admin key" in response.text


def test_invalid_admin_key():
    response = client.get(
        "/view-all-users?key=wrong-key"
    )

    assert response.status_code == 401
    assert "Invalid admin key" in response.text