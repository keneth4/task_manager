from datetime import datetime
from fastapi.testclient import TestClient
from sqlmodel import Session
from app.models import Task
from . import session_fixture, client_fixture # noqa: F401


def test_delete_task(session: Session, client: TestClient):
    # Create a task
    task = Task(
        title="Test Task",
        description="This is a test task.",
        due_date=datetime(2022, 12, 31),
    )

    session.add(task)
    session.commit()

    # Delete the task
    response = client.delete(f"/tasks/{task.id}")

    # Get the task from the database
    task_in_db = session.get(Task, task.id)

    assert response.status_code == 200
    assert response.json() == {"ok": True}
    assert task_in_db is None



def test_delete_task_invalid_task_id(client: TestClient):
    response = client.delete("/tasks/invalid-uuid")
    assert response.status_code == 422


def test_delete_task_not_found(client: TestClient):
    response = client.delete("/tasks/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
