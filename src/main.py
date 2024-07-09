from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from src.routes.todo_views import router as router_todo
from .routes.auth_views import router as router_auth
from src.database import Base, engine, get_db
from .services.crud_todo import TodoRepo

templates = Jinja2Templates(directory="src/templates")

app = FastAPI(title="FastAPI - APP", description="Academy ITStep")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_todo)
app.include_router(router_auth)




@app.get("/todos")
async def todo_main(request: Request, db: Session = Depends(get_db)):
    todos = TodoRepo.get_todos(db)
    return templates.TemplateResponse("index.html", {"request": request, "todos": todos})

# @app.on_event("startup")
# async def on_startup():
#     Base.metadata.create_all(bind=engine)


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(".main:src", reload=True)








