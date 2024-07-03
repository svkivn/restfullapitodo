from fastapi import APIRouter, Depends, Path, status, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas.todo import SchemaBaseTodo, SchemaTodo, SchemaUpdateTodo
from services.crud_todo import TodoRepo

router = APIRouter(prefix="/todo", tags=["Todo RESTfull API"])


@router.post("/", response_model=SchemaTodo, status_code=201)
def create_todo(todo_create: SchemaBaseTodo, db: Session = Depends(get_db)):
    db_todo = TodoRepo.create_todo(db, todo_create)
    return db_todo


@router.get("/", response_model=list[SchemaTodo])
def read_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    todos = TodoRepo.get_todos(db, skip=skip, limit=limit)
    return todos


@router.get("/{id}", response_model=SchemaTodo)
def read_todo(id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    todo = TodoRepo.get_todo_id(db=db, id=id)
    if not todo:
        raise HTTPException(status_code=404, detail=f"Todo with {id} not found")
    return todo


@router.put("/{id}/", response_model=SchemaTodo, status_code=status.HTTP_200_OK)
def update_note(payload: SchemaUpdateTodo, db: Session = Depends(get_db), id: int = Path(..., gt=0)):
    todo = TodoRepo.get_todo_id(db=db, id=id)
    if not todo:
        raise HTTPException(status_code=404, detail=f"Todo with {id} not found")
    todo = TodoRepo.update_todo(db=db, todo=todo, payload=payload)
    return todo


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(db: Session = Depends(get_db), id: int = Path(..., gt=0)):
    todo = TodoRepo.get_todo_id(db=db, id=id)
    if not todo:
        raise HTTPException(status_code=404, detail=f"Todo with {id} not found")
    TodoRepo.delete_todo(db=db, todo=todo)
