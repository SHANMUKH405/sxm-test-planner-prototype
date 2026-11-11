from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_demo_catalogue_has_three_separate_tests() -> None:
    response = client.get("/api/catalog")
    assert response.status_code == 200
    catalogue = response.json()
    assert len(catalogue) == 3
    assert len({test["id"] for test in catalogue}) == 3


def test_incompatible_target_is_rejected() -> None:
    test_id = client.get("/api/catalog").json()[0]["id"]
    response = client.post(
        "/api/runs",
        json={"name": "Blocked run", "test_ids": [test_id], "target_id": "headunit-placeholder"},
    )
    assert response.status_code == 409
