from fastapi import FastAPI
from routes.todo_views import router as router_todo
from database import Base, engine

app = FastAPI()
app.include_router(router_todo)

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)








