from sqlalchemy.orm import Session

from models.todo import Todo
from schemas.todo import SchemaBaseTodo, SchemaUpdateTodo, SchemaTodo


def get_todo_id(db: Session, id: int):
    return db.query(Todo).filter(Todo.id == id).first()


def get_todos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Todo).offset(skip).limit(limit).all()


def create_todo(db: Session, todo_create: SchemaBaseTodo) -> Todo:
    db_todo = Todo(**todo_create.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


#####################

def update_todo(db: Session, todo: Todo, payload: SchemaUpdateTodo) -> Todo:
    payload_dict = payload.model_dump(exclude_unset=True)
    if not payload_dict:
        return todo
    for field, value in payload_dict.items(): #.dict(exclude_unset=True).items()
        setattr(todo, field, value)
    db.commit()
    db.refresh(todo)
    return todo


def delete_todo(db: Session, todo: Todo) -> Todo:
    db.delete(todo)
    db.commit()
    return todo
