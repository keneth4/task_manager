import uuid
from datetime import datetime
from fastapi import HTTPException, Depends, Query
from . import app, logger, get_session
from app.models import Task, TaskPublic, TaskCreate, TaskUpdate, StatusEnum
from sqlmodel import Session, select


STATUS_CHOICES_REGEX = r"|".join([status.value for status in StatusEnum])


@app.get("/ping")
async def ping():
    return {"message": "pong"}


@app.post("/tasks/", response_model=TaskPublic)
def create_task(*, session: Session = Depends(get_session), task: TaskCreate):
    db_task = Task.model_validate(task)
    if db_task.due_date:
        db_task.due_date = db_task.due_date.replace(hour=0, minute=0, second=0, microsecond=0)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    logger.info(f"Task with ID \[{db_task.id}] created: '{db_task.title}'.")
    return db_task


@app.get("/tasks/", response_model=list[TaskPublic])
def read_tasks(
    *,
    session: Session = Depends(get_session),
    status: str = Query(None, title="Status filter", regex=STATUS_CHOICES_REGEX),
    due_date: str = Query(None, title="Due date filter"),
):
    filter = []
    if status:
        filter.append(Task.status == StatusEnum(status))
    if due_date:
        try:
            due_date = datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
        filter.append(Task.due_date == due_date)
    tasks = session.exec(select(Task).where(*filter)).all()
    return tasks


@app.get("/tasks/{task_id}", response_model=TaskPublic)
def read_task(*, session: Session = Depends(get_session), task_id: uuid.UUID):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}", response_model=TaskPublic)
def update_task(
    *,
    session: Session = Depends(get_session),
    task_id: uuid.UUID,
    task: TaskUpdate,
):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    task_data = task.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    logger.info(f"Task with ID \[{db_task.id}] updated: '{db_task.title}'.")
    return db_task


@app.delete("/tasks/{task_id}")
def delete_task(*, session: Session = Depends(get_session), task_id: uuid.UUID):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(db_task)
    session.commit()
    logger.info(f"Task with ID \[{db_task.id}] deleted: '{db_task.title}'.")
    return {"ok": True}