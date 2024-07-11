from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from schemas.user import UserCreate, UserLogin, User as UserSchema
from services.auth import create_access_token

router = APIRouter(prefix="/users", tags=["User Auth"])


@router.post("/register", response_model=UserSchema)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    user = User(username=payload.username, email=payload.email, password=payload.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/", response_model=list[UserSchema])
def register_user(db: Session = Depends(get_db)):
    stmt = select(User)
    users = db.scalars(stmt).all()
    return users


@router.post("/login")
def login_user(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.scalar(select(User).filter_by(email=payload.email))
    if not user or not user.password == payload.password:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    token = create_access_token(subject=user.id)
    return {"access_token": token, "token_type": "bearer"}

