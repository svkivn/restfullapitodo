from typing import Optional

from pydantic import BaseModel, Field


class SchemaBaseTodo(BaseModel):
    title: str
    complete: bool = False


class SchemaTodo(SchemaBaseTodo):
    id: int

    class Config:
        from_attributes = True


class SchemaUpdateTodo(BaseModel):
    title: str | None = None
    complete: bool | None = None


class ListTodosSchema(BaseModel):
    tasks: list[SchemaTodo]

    class Config:
        orm_mode = True
