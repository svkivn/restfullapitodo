from typing import Optional

from pydantic import BaseModel


class SchemaBaseTodo(BaseModel):
    title: str
    complete: bool = False


class SchemaUpdateTodo(BaseModel):
    title: str | None = None
    complete: Optional[bool] = None


class SchemaTodo(SchemaBaseTodo):
    id: int

    class Config:
        from_attributes = True
        # orm_mode = True



