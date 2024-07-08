from pydantic import BaseModel, EmailStr, Field


class BaseUser(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=4)


class UserCreate(BaseUser):
    password: str  # = Field(..., exclude=True)


class User(BaseUser):
    id: int


    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
