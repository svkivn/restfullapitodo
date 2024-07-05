from sqlalchemy import String, Enum
import enum
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Todo(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    complete: Mapped[bool | None] = mapped_column(default=False)

    #type: Mapped[TypeTodo] = mapped_column(Enum(TypeTodo), nullable=True)



class TypeTodo(enum.Enum):
    in_progress = 'in progress'
    not_start = 'not start'
    pause = 'pause'
