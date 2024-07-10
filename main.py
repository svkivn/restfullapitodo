from fastapi import FastAPI, Request, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from routes.todo_views import router as router_todo

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from services import crud_todo

templates = Jinja2Templates(directory="templates")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router_todo)

@app.get("/", response_class=HTMLResponse)
def get_index(request: Request, db: Session = Depends(get_db)):
    todos = crud_todo.get_todos(db=db)
    return templates.TemplateResponse(request=request, name="index.html", context={"todos": todos})

from fastapi.security import HTTPBasic, HTTPBasicCredentials
basic = HTTPBasic()

users_session_DB = {}

@app.get("/who")
def get_user(creds: HTTPBasicCredentials =Depends(basic)):
    if creds.username =="admin" and creds.password=="1235":
        return {"username": creds.username, "password": creds.password}
    raise HTTPException(status_code=401)

from fastapi.responses import RedirectResponse

@app.get("/login")
def s_login(username: str, password: str):
    if username == "admin" and password == "1235":
        responce = RedirectResponse("/", status_code=302)
        responce.set_cookie(key="session_id", value="sasjsderjkngsmajdkasjdh")
        users_session_DB["sasjsderjkngsmajdkasjdh"] = {"username" : "admin", "password" : "1235"}
        return responce
    raise HTTPException(status_code=401)


@app.get("/logout")
def s_logout(responce: Response):
    responce.delete_cookie(key="session_id")
    users_session_DB.pop("sasjsderjkngsmajdkasjdh", None)
    return {"status": "logged out"}

Base.metadata.create_all(bind=engine)
