from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models.todo import Todo
from ..schemas.todo import SchemaBaseTodo, SchemaUpdateTodo


class TodoRepo:
    """Class Repo for ORM-model Todo"""

    @staticmethod
    def get_todo_id(db: Session, id: int):
        stmt = select(Todo).filter_by(id=id)
        todo = db.scalar(stmt)  # ~ todo = db.scalars(stmt).one_or_none()
        return todo

    @staticmethod
    def get_todos(db: Session, skip: int = 0, limit: int = 100):
        stmt = select(Todo).offset(skip).limit(limit)
        todos = db.scalars(stmt).all()
        return todos

    @staticmethod
    def create_todo(db: Session, payload: SchemaBaseTodo) -> Todo:
        db_todo = Todo(**payload.dict())
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return db_todo

    @staticmethod
    def update_todo(db: Session, todo: Todo, payload: SchemaUpdateTodo) -> Todo:
        payload_dict = payload.model_dump(exclude_unset=True)
        if not payload_dict:
            return todo
        for field, value in payload_dict.items():  # payload.dict(exclude_unset=True).items()
            setattr(todo, field, value)
        db.commit()
        db.refresh(todo)
        return todo

    @staticmethod
    def delete_todo(db: Session, todo: Todo):
        db.delete(todo)
        db.commit()
