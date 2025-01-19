import uuid
from fastapi import HTTPException, Depends, Query
from . import app, logger, get_session
from app.models import Task, TaskPublic, TaskCreate, TaskUpdate
from sqlmodel import Session, select


@app.get("/ping")
async def ping():
    return {"message": "pong"}


@app.post("/tasks/", response_model=TaskPublic)
def create_task(*, session: Session = Depends(get_session), task: TaskCreate):
    db_task = Task.model_validate(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    logger.info(f"Task with ID [{db_task.id}] created: '{db_task.title}'.")
    return db_task


@app.get("/tasks/", response_model=list[TaskPublic])
def read_tasks(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=10, le=10),
):
    tasks = session.exec(select(Task).offset(offset).limit(limit)).all()
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
    logger.info(f"Task with ID [{db_task.id}] updated: '{db_task.title}'.")
    return db_task


@app.delete("/tasks/{task_id}")
def delete_task(*, session: Session = Depends(get_session), task_id: uuid.UUID):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(db_task)
    session.commit()
    logger.info(f"Task with ID [{db_task.id}] deleted: '{db_task.title}'.")
    return {"ok": True}