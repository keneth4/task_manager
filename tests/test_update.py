from datetime import date
from sqlmodel import Session
from fastapi.testclient import TestClient
from app.models import Task, StatusEnum
from . import session_fixture, client_fixture # noqa: F401


def test_update_task(session: Session, client: TestClient):
    # Create a task
    task = Task(
        title="Test Task",
        description="This is a test task.",
        due_date=date(2022, 12, 31),
    )

    session.add(task)
    session.commit()

    # Update the task
    updated_data = {
        "title": "Updated Task",
        "description": "This is an updated task.",
        "status": "in-progress",
        "due_date": "2023-12-31",
    }
    response = client.put(f"/tasks/{task.id}", json=updated_data)
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["title"] == updated_data["title"]
    assert response_data["description"] == updated_data["description"]
    assert response_data["status"] == updated_data["status"]
    assert response_data["due_date"] == updated_data["due_date"]
    assert response_data["id"] is not None


def test_update_task_no_data(session: Session, client: TestClient):
    # Create a task
    task = Task(
        title="Test Task",
        description="This is a test task.",
        due_date=date(2022, 12, 31),
    )

    session.add(task)
    session.commit()

    # Update the task with no data
    response = client.put(f"/tasks/{task.id}", json={})
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["title"] == task.title
    assert response_data["description"] == task.description
    assert response_data["status"] == task.status
    assert response_data["due_date"] == str(task.due_date)
    assert response_data["id"] is not None


def test_update_task_invalid_task_id(client: TestClient):
    response = client.put("/tasks/invalid-uuid", json={})
    assert response.status_code == 422


def test_update_task_not_found(client: TestClient):
    response = client.put("/tasks/00000000-0000-0000-0000-000000000000", json={})
    assert response.status_code == 404


def test_update_task_invalid_title_length(session: Session, client: TestClient):
    # Create a task
    task = Task(
        title="Test Task",
        description="This is a test task.",
        due_date=date(2022, 12, 31),
    )

    session.add(task)
    session.commit()

    # Update the task with invalid title length
    updated_data = {
        "title": "A" * 101,
        "description": "This is an updated task.",
        "status": "in-progress",
        "due_date": "2023-12-31",
    }
    response = client.put(f"/tasks/{task.id}", json=updated_data)
    assert response.status_code == 422


def test_update_task_invalid_status(session: Session, client: TestClient):
    # Create a task
    task = Task(
        title="Test Task",
        description="This is a test task.",
        due_date=date(2022, 12, 31),
    )

    session.add(task)
    session.commit()

    # Update the task with invalid status
    updated_data = {
        "title": "Updated Task",
        "description": "This is an updated task.",
        "status": "invalid-status",
        "due_date": "2023-12-31",
    }
    response = client.put(f"/tasks/{task.id}", json=updated_data)
    assert response.status_code == 422


def test_update_task_invalid_due_date(session: Session, client: TestClient):
    # Create a task
    task = Task(
        title="Test Task",
        description="This is a test task.",
        due_date=date(2022, 12, 31),
    )

    session.add(task)
    session.commit()

    # Update the task with invalid due date
    updated_data = {
        "title": "Updated Task",
        "description": "This is an updated task.",
        "status": "in-progress",
        "due_date": "2023-12-33",
    }
    response = client.put(f"/tasks/{task.id}", json=updated_data)
    assert response.status_code == 422
