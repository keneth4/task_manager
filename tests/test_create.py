from fastapi.testclient import TestClient
from . import session_fixture, client_fixture # noqa: F401


def test_create_task(client: TestClient):
    data = {
        "title": "Test Task",
        "description": "This is a test task.",
        "status": "pending",
        "due_date": "2022-12-31",
    }
    response = client.post("/tasks/", json=data)
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["title"] == data["title"]
    assert response_data["description"] == data["description"]
    assert response_data["status"] == data["status"]
    assert response_data["due_date"] == data["due_date"]
    assert response_data["id"] is not None


def test_create_task_only_title(client: TestClient):
    data = {
        "title": "Test Task",
    }
    response = client.post("/tasks/", json=data)
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["title"] == data["title"]
    assert response_data["description"] is None
    assert response_data["status"] == "pending"
    assert response_data["due_date"] is None
    assert response_data["id"] is not None


def test_create_task_no_title(client: TestClient):
    data = {
        "description": "This is a test task.",
        "status": "pending",
        "due_date": "2022-12-31",
    }
    response = client.post("/tasks/", json=data)
    assert response.status_code == 422


def test_create_task_invalid_title_length(client: TestClient):
    data = {
        "title": "A" * 101,
        "description": "This is a test task.",
        "status": "pending",
        "due_date": "2022-12-31",
    }
    response = client.post("/tasks/", json=data)
    assert response.status_code == 422


def test_create_task_invalid_status(client: TestClient):
    data = {
        "title": "Test Task",
        "description": "This is a test task.",
        "status": "invalid",
        "due_date": "2022-12-31",
    }
    response = client.post("/tasks/", json=data)
    assert response.status_code == 422


def test_create_task_invalid_due_date(client: TestClient):
    data = {
        "title": "Test Task",
        "description": "This is a test task.",
        "status": "pending",
        "due_date": "2022-12-33",
    }
    response = client.post("/tasks/", json=data)
    assert response.status_code == 422
