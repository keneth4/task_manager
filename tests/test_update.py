from fastapi.testclient import TestClient
from . import session_fixture, client_fixture # noqa: F401


def test_update_task(client: TestClient):
    # Create a task
    data = {
        "title": "Test Task",
        "description": "This is a test task.",
        "status": "pending",
        "due_date": "2022-12-31",
    }
    response = client.post("/tasks/", json=data)
    response_data = response.json()

    # Update the task
    updated_data = {
        "title": "Updated Task",
        "description": "This is an updated task.",
        "status": "in-progress",
        "due_date": "2023-12-31",
    }
    response = client.put(f"/tasks/{response_data['id']}", json=updated_data)
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["title"] == updated_data["title"]
    assert response_data["description"] == updated_data["description"]
    assert response_data["status"] == updated_data["status"]
    assert response_data["due_date"] == updated_data["due_date"] + "T00:00:00"
    assert response_data["id"] is not None


def test_update_task_no_data(client: TestClient):
    # Create a task
    data = {
        "title": "Test Task",
        "description": "This is a test task.",
        "status": "pending",
        "due_date": "2022-12-31",
    }
    response = client.post("/tasks/", json=data)
    response_data = response.json()

    # Update the task with no data
    response = client.put(f"/tasks/{response_data['id']}", json={})
    assert response.status_code == 200
    assert response.json() == response_data


def test_update_task_invalid_task_id(client: TestClient):
    response = client.put("/tasks/invalid-uuid", json={})
    assert response.status_code == 422


def test_update_task_not_found(client: TestClient):
    response = client.put("/tasks/00000000-0000-0000-0000-000000000000", json={})
    assert response.status_code == 404


def test_update_task_invalid_title_length(client: TestClient):
    # Create a task
    data = {
        "title": "Test Task",
        "description": "This is a test task.",
        "status": "pending",
        "due_date": "2022-12-31",
    }
    response = client.post("/tasks/", json=data)
    response_data = response.json()

    # Update the task with invalid title length
    updated_data = {
        "title": "A" * 101,
        "description": "This is an updated task.",
        "status": "in-progress",
        "due_date": "2023-12-31",
    }
    response = client.put(f"/tasks/{response_data['id']}", json=updated_data)
    assert response.status_code == 422


def test_update_task_invalid_status(client: TestClient):
    # Create a task
    data = {
        "title": "Test Task",
        "description": "This is a test task.",
        "status": "pending",
        "due_date": "2022-12-31",
    }
    response = client.post("/tasks/", json=data)
    response_data = response.json()

    # Update the task with invalid status
    updated_data = {
        "title": "Updated Task",
        "description": "This is an updated task.",
        "status": "invalid-status",
        "due_date": "2023-12-31",
    }
    response = client.put(f"/tasks/{response_data['id']}", json=updated_data)
    assert response.status_code == 422


def test_update_task_invalid_due_date(client: TestClient):
    # Create a task
    data = {
        "title": "Test Task",
        "description": "This is a test task.",
        "status": "pending",
        "due_date": "2022-12-31",
    }
    response = client.post("/tasks/", json=data)
    response_data = response.json()

    # Update the task with invalid due date
    updated_data = {
        "title": "Updated Task",
        "description": "This is an updated task.",
        "status": "in-progress",
        "due_date": "2023-12-33",
    }
    response = client.put(f"/tasks/{response_data['id']}", json=updated_data)
    assert response.status_code == 422
