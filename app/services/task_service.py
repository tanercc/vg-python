from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.user import User
from app.repositories.task_repository import (
    task_repository,
)
from app.schemas.task import TaskCreate, TaskUpdate
from app.core.logging import logger


class TaskService:
    def list_tasks(
        self,
        db: Session,
        current_user: User,
    ) -> list[Task]:
        if current_user.is_admin:
            return task_repository.get_all(db)

        return task_repository.get_for_user(
            db,
            current_user.id,
        )

    def get_task(
        self,
        db: Session,
        task_id: int,
        current_user: User,
    ) -> Task:
        task = task_repository.get_by_id(
            db,
            task_id,
        )

        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        self._ensure_access(
            task,
            current_user,
        )

        return task

    def create_task(
        self,
        db: Session,
        data: TaskCreate,
        current_user: User,
    ) -> Task:
        try:
            task = task_repository.create(
                db,
                current_user.id,
                data,
            )

            db.commit()
            db.refresh(task)

            return task

        except Exception:
            db.rollback()

            logger.exception(
                "Task creation failed",
                extra={
                    "user_id": current_user.id,
                },
            )
            
            raise


    def update_task(
        self,
        db: Session,
        task_id: int,
        data: TaskUpdate,
        current_user: User,
    ) -> Task:
        task = self.get_task(
            db,
            task_id,
            current_user,
        )

        try:
            task_repository.update(
                task,
                data,
            )

            db.commit()
            db.refresh(task)

            return task

        except Exception:
            db.rollback()

            logger.exception(
                "Task update failed",
                extra={
                    "user_id": current_user.id,
                    "task_id": task_id,
                },
            )
            
            raise

    def delete_task(
        self,
        db: Session,
        task_id: int,
        current_user: User,
    ) -> None:
        task = self.get_task(
            db,
            task_id,
            current_user,
        )

        try:
            task_repository.delete(
                db,
                task,
            )

            db.commit()

        except Exception:
            db.rollback()

            logger.exception(
                "Task deletion failed",
                extra={
                    "user_id": current_user.id,
                    "task_id": task_id,
                },
            )
            
            raise

    def _ensure_access(
        self,
        task: Task,
        current_user: User,
    ) -> None:
        if current_user.is_admin:
            return

        if task.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not allowed to access this task",
            )

task_service = TaskService()