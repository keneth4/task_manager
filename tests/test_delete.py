from fastapi.testclient import TestClient
from . import session_fixture, client_fixture # noqa: F401


def test_delete_task(client: TestClient):
    # Create a task
    data = {
        "title": "Test Task",
        "description": "This is a test task.",
        "status": "pending",
        "due_date": "2022-12-31",
    }
    response = client.post("/tasks/", json=data)
    response_data = response.json()

    # Delete the task
    response = client.delete(f"/tasks/{response_data['id']}")
    assert response.status_code == 200
    assert response.json() == {"ok": True}


def test_delete_task_invalid_task_id(client: TestClient):
    response = client.delete("/tasks/invalid-uuid")
    assert response.status_code == 422


def test_delete_task_not_found(client: TestClient):
    response = client.delete("/tasks/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
