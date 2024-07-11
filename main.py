from fastapi import FastAPI, Request, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from routes.todo_views import router as router_todo
from routes.user_views import router as router_user

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from services import crud_todo
from fastapi.responses import RedirectResponse

templates = Jinja2Templates(directory="templates")

app = FastAPI()
app.include_router(router_user)
app.include_router(router_todo)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




@app.get("/", response_class=HTMLResponse)
def get_index(request: Request, db: Session = Depends(get_db)):
    todos = crud_todo.get_todos(db=db)
    return templates.TemplateResponse(request=request, name="index.html", context={"todos": todos})


# from fastapi.security import HTTPBasic, HTTPBasicCredentials
#
# basic = HTTPBasic()
#
# users_session_DB = {}
#
#
# @app.get("/who")
# def get_user(creds: HTTPBasicCredentials = Depends(basic)):
#     if creds.username == "admin" and creds.password == "1235":
#         return {"username": creds.username, "password": creds.password}
#     raise HTTPException(status_code=401)
#
#
#
# @app.get("/login")
# def s_login(username: str, password: str):
#     if username == "admin" and password == "1235":
#         responce = RedirectResponse("/profile", status_code=302)
#         responce.set_cookie(key="session_id", value="sasjsderjkngsmajdkasjdh")
#         users_session_DB["sasjsderjkngsmajdkasjdh"] = \
#             {"username": "admin", "password": "1235"}
#         return responce
#     raise HTTPException(status_code=401)
#
#
# @app.get("/logout")
# def s_logout(responce: Response):
#     responce.delete_cookie(key="session_id")
#     users_session_DB.pop("sasjsderjkngsmajdkasjdh", None)
#     return {"status": "logged out"}
#
#
# ########## 1
# def get_auth_user(request: Request):
#     """verify that user has a valid session"""
#     session_value = request.cookies.get("session_id")
#     if not session_value:
#         raise HTTPException(status_code=401)
#     if session_value not in users_session_DB:
#         raise HTTPException(status_code=403)
#     return users_session_DB.get(session_value)
#
#
# @app.get("/profile")
# async def secret(dependencies=Depends(get_auth_user)):
#     return {"secret": "info", "dependencies": dependencies}



#Base.metadata.create_all(bind=engine)

