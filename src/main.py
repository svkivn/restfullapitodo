from fastapi import FastAPI
from .routes.todo_views import router as router_todo
from .database import Base, engine

app = FastAPI(title="FastAPI - APP", description="Academy ITStep")
app.include_router(router_todo)



@app.on_event("startup")
async def on_startup():
    Base.metadata.create_all(bind=engine)


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(".main:src", reload=True)








