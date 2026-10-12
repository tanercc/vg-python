from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


class TaskRepository:
    def get_by_id(
        self,
        db: Session,
        task_id: int,
    ) -> Task | None:
        return db.get(Task, task_id)

    def get_for_user(
        self,
        db: Session,
        user_id: int,
    ) -> list[Task]:
        statement = select(Task).where(
            Task.user_id == user_id
        )

        return list(
            db.scalars(statement).all()
        )

    def get_all(
        self,
        db: Session,
    ) -> list[Task]:
        statement = select(Task)

        return list(
            db.scalars(statement).all()
        )

    def create(
        self,
        db: Session,
        user_id: int,
        data: TaskCreate,
    ) -> Task:
        task = Task(
            title=data.title,
            description=data.description,
            status=data.status,
            user_id=user_id,
        )

        db.add(task)

        return task

    def update(
        self,
        task: Task,
        data: TaskUpdate,
    ) -> Task:
        update_data = data.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(task, field, value)

        return task

    def delete(
        self,
        db: Session,
        task: Task,
    ) -> None:
        db.delete(task)


task_repository = TaskRepository()