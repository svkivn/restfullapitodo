# routers/auth.py or authentication.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.user import User as UserSchema, UserCreate as UserCreateSchema
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



# @router.post("/login")
# def login_user(payload: LoginUser, db: Session = Depends(get_db)):
#     """
#     Login user based on email and password
#     """
#     if not payload.email:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Please add Phone number",
#         )
#
#     user = get_user(db, payload.email)
#     token = create_access_token(user.id, timedelta(minutes=30))
#     refresh = create_refresh_token(user.id, timedelta(minutes=1008))
#
#     return {'access_token': token, 'token_type': 'bearer', 'refresh_token': refresh, "user_id": user.id}
