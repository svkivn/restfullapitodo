# routers/auth.py or authentication.py
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.user import User as UserSchema, UserCreate as UserCreateSchema, UserLogin, User
from ..services.auth import create_access_token, get_current_user_id, get_current_user
from ..services.crud_user import RepoUsers

router = APIRouter(prefix="/auth", tags=["Authentication"])


# Register new user using email, username, password
@router.post("/register", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreateSchema, db: Session = Depends(get_db)):
    user = RepoUsers.get_user(db, payload.email)

    if user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"User with {payload.email} already exists",
        )
    user = RepoUsers.create_user(db, payload)
    return user


# get_users
@router.get("/users", response_model=list[UserSchema])
def get_users(db: Session = Depends(get_db)):
    users = RepoUsers.get_all_users(db)
    return users


@router.post("/login")
def login_user(payload: UserLogin, db: Session = Depends(get_db)):
    """
    Login user based on email and password
    """
    user = RepoUsers.get_user(db, payload.email)
    if not user or not user.check_password(payload.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    token = create_access_token(user.id, timedelta(minutes=30))
    return {'access_token': token, 'token_type': 'bearer', "user_id": user.id}


@router.get("/users/me", response_model=UserSchema)
def read_users_me(db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    """
    Get current user details by id from the database
    """

    current_user = RepoUsers.get_user_by_id(db=db, id=current_user_id)
    return current_user


@router.get("/users/me2", response_model=UserSchema)
def read_users_me2(current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found")
    return current_user
