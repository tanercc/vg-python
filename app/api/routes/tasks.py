from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.task import (
    TaskCreate,
    TaskResponse,
    TaskUpdate,
)
from app.services.task_service import task_service


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.get(
    "",
    response_model=list[TaskResponse],
)
def list_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return task_service.list_tasks(
        db,
        current_user,
    )


@router.post(
    "",
    response_model=TaskResponse,
    status_code=201,
)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return task_service.create_task(
        db,
        task,
        current_user,
    )


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return task_service.get_task(
        db,
        task_id,
        current_user,
    )


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return task_service.update_task(
        db,
        task_id,
        task_update,
        current_user,
    )


@router.delete(
    "/{task_id}",
    status_code=204,
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task_service.delete_task(
        db,
        task_id,
        current_user,
    )