from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

#SQLALCHEMY_DATABASE_URL = "sqlite:///data.db"
SQLALCHEMY_DATABASE_URL = "postgresql://data_todo_user:KKk7fNOtD2gq9yNtcVGJuLNWYfhNXlTQ@dpg-cq3a4jjqf0us73ddlnq0-a.oregon-postgres.render.com/data_todo"
engine = create_engine(SQLALCHEMY_DATABASE_URL,  echo=False) #connect_args={"check_same_thread": False},

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    print(0)
    try:
        yield db
        print(1)
    except Exception as e:
        print(2)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"{e}")
    finally:
        db.close()
        print("closed")

# from sqlalchemy.ext.declarative import declarative_base
# Base = declarative_base()
