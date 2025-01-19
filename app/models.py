from typing import Optional
from datetime import datetime, timezone

import uuid
from enum import Enum

from sqlmodel import Field, SQLModel
from sqlalchemy import String, Index
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.sql import func
from pydantic import Field as PydanticField


class StatusEnum(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"


class TaskBase(SQLModel):
    __table_args__ = (
        Index("ix_task_status", "status"),  # Explicitly add an index for the status column
    )
    title: str = Field(sa_column=String(length=100))
    description: Optional[str] = None
    status: StatusEnum = Field(
        default_factory=lambda: StatusEnum.PENDING,
        sa_column=SQLAlchemyEnum(StatusEnum),
        )
    due_date: Optional[datetime] = Field(default=None, index=True)


class Task(TaskBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"server_default": func.now()}
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": func.now()}
    )


class TaskCreate(TaskBase):
    title: str = PydanticField(max_length=100)


class TaskPublic(TaskBase):
    id: uuid.UUID
    title: str
    description: Optional[str] = None
    status: StatusEnum
    due_date: Optional[datetime] = None


class TaskUpdate(SQLModel):
    title: Optional[str] = PydanticField(max_length=100, default=None)
    description: Optional[str] = None
    status: Optional[StatusEnum] = None
    due_date: Optional[datetime] = None