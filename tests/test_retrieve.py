from fastapi.testclient import TestClient
from . import session_fixture, client_fixture # noqa: F401


def test_get_all_tasks(client: TestClient):
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert response.json() == []


def test_get_task_by_uuid(client: TestClient):
    # Create a task
    data = {
        "title": "Test Task",
        "description": "This is a test task.",
        "status": "pending",
        "due_date": "2022-12-31",
    }
    response = client.post("/tasks/", json=data)
    response_data = response.json()

    # Get the task by UUID
    response = client.get(f"/tasks/{response_data['id']}")
    assert response.status_code == 200
    data["id"] = response_data["id"]
    data["due_date"] += "T00:00:00"
    assert response.json() == data


def test_get_task_by_using_status_filter(client: TestClient):
    # Create a task with status "in-progress"
    data = {
        "title": "Test Task",
        "description": "This is a test task.",
        "status": "in-progress",
        "due_date": "2022-12-31",
    }
    response = client.post("/tasks/", json=data)
    response_data = response.json()

    # Get the task by using status filter
    response = client.get("/tasks/?status=in-progress")
    assert response.status_code == 200
    data["id"] = response_data["id"]
    data["due_date"] += "T00:00:00"
    assert response.json() == [data]


def test_get_task_by_using_due_date_filter(client: TestClient):
    # Create a task with due date "2025-12-31"
    data = {
        "title": "Test Task",
        "description": "This is a test task.",
        "status": "pending",
        "due_date": "2025-12-31",
    }
    response = client.post("/tasks/", json=data)
    response_data = response.json()

    # Get the task by using due date filter
    response = client.get("/tasks/?due_date=2025-12-31")
    assert response.status_code == 200
    data["id"] = response_data["id"]
    data["due_date"] += "T00:00:00"
    assert response.json() == [data]


def test_get_task_by_using_both_filters(client: TestClient):
    # Create a task with status "completed" and due date "2020-12-31"
    data = {
        "title": "Test Task",
        "description": "This is a test task.",
        "status": "completed",
        "due_date": "2020-12-31",
    }
    response = client.post("/tasks/", json=data)
    response_data = response.json()

    # Get the task by using both filters
    response = client.get("/tasks/?status=completed&due_date=2020-12-31")
    assert response.status_code == 200
    data["id"] = response_data["id"]
    data["due_date"] += "T00:00:00"
    assert response.json() == [data]


def test_get_task_by_non_existent_uuid(client: TestClient):
    response = client.get("/tasks/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_get_task_by_invalid_uuid(client: TestClient):
    response = client.get("/tasks/invalid-uuid")
    assert response.status_code == 422


def test_get_task_by_invalid_status_filter(client: TestClient):
    response = client.get("/tasks/?status=invalid-status")
    assert response.status_code == 422


def test_get_task_by_invalid_due_date_filter(client: TestClient):
    response = client.get("/tasks/?due_date=invalid-date")
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid date format. Use YYYY-MM-DD."}
