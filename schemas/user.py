from pydantic import BaseModel, Field, EmailStr


class BaseUser(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=4)


class UserCreate(BaseUser):
    password: str


class User(BaseUser):
    id: int

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
