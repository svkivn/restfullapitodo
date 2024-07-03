from fastapi import FastAPI, Depends, Path, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal, Base, engine
from schemas.todo import SchemaTodo, SchemaBaseTodo, SchemaUpdateTodo
from services import crud_todo as crud

app = FastAPI()
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    print(0)
    try:
        yield db
        print(1)
    except Exception as e:
        print(2)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"{e}")
    finally:
        db.close()
        print("closed")


@app.post("/todos/", response_model=SchemaTodo, status_code=201)
def create_todo(todo_create: SchemaBaseTodo, db: Session = Depends(get_db)):
    db_todo = crud.create_todo(db, todo_create)
    return db_todo


@app.get("/todos/", response_model=list[SchemaTodo])
def read_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    todos = crud.get_todos(db, skip=skip, limit=limit)
    return todos


#############
@app.get("/todos/{id}", response_model=SchemaTodo)
def read_todo(id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    todo = crud.get_todo_id(db=db, id=id)
    if not todo:
        raise HTTPException(status_code=404, detail=f"Todo with {id} not found")
    return todo


@app.put("/todos/{id}/", response_model=SchemaTodo, status_code=status.HTTP_200_OK)
def update_note(payload: SchemaUpdateTodo, db: Session = Depends(get_db), id: int = Path(..., gt=0)):
    todo = crud.get_todo_id(db=db, id=id)
    if not todo:
        raise HTTPException(status_code=404, detail=f"Todo with {id} not found")
    todo = crud.update_todo(db=db, todo=todo, payload=payload)
    return todo


@app.delete("/todos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(db: Session = Depends(get_db), id: int = Path(..., gt=0)):
    todo = crud.get_todo_id(db=db, id=id)
    if not todo:
        raise HTTPException(status_code=404, detail=f"Todo with {id} not found")
    crud.delete_todo(db=db, todo=todo)

    #return Response(status_code=status.HTTP_204_NO_CONTENT)

