from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_query_validation():
    response = client.post(
        "/query",
        json={}
    )

    assert response.status_code == 422
