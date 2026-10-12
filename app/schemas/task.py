from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


TaskStatus = Literal[
    "pending",
    "in_progress",
    "completed",
]


class TaskCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=200,
    )

    description: str | None = Field(
        default=None,
        max_length=2000,
    )

    status: TaskStatus = "pending"


class TaskUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
    )

    description: str | None = Field(
        default=None,
        max_length=2000,
    )

    status: TaskStatus | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: TaskStatus
    user_id: int

    model_config = ConfigDict(
        from_attributes=True,
    )