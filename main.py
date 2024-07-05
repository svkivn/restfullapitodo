from fastapi import FastAPI
from database import Base, engine
from routes.todo_views import router as router_todo

app = FastAPI()
app.include_router(router_todo)

Base.metadata.create_all(bind=engine)





