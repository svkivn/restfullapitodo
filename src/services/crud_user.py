from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas.user import UserCreate

class RepoUsers:

    @staticmethod
    def get_user(db: Session, email: EmailStr) -> User | None:
        '''return db.query(User).filter(User.email == email).first()'''

        stmt = select(User).filter_by(email=email)
        user = db.scalar(stmt)  # ~ todo = db.scalars(stmt).one_or_none()
        return user

    @staticmethod
    def get_all_users(db: Session) -> list[User]:
        stmt = select(User)
        users = db.scalars(stmt).all()
        return users

    @staticmethod
    def create_user(db: Session, payload: UserCreate):
        db_user = User(username=payload.username, email=payload.email,  password=payload.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

