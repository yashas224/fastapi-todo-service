from typing import Annotated

from fastapi import APIRouter
from fastapi import HTTPException, status, Path, Depends
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import select
from models import Users
from routers.auth import get_current_user
from dependencies import db_dependency
from models import Todos

router = APIRouter(dependencies=[Depends(get_current_user)])

user_dependency = Annotated[Users, Depends(get_current_user)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3, max_length=30)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, le=5)
    complete: bool

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Gardening",
                "description": "Need to water plants",
                "priority": 3,
                "complete": 0
            }
        }
    )


@router.get("/health")
def health():
    return {"message": "Todo service healthy"}


@router.get("/todos")
async def read_all(db_session: db_dependency, user_dependency: user_dependency):
    return db_session.scalars(select(Todos).where(Todos.user_id == user_dependency.id)).all()


@router.get("/todos/{id}", status_code=status.HTTP_200_OK)
def get_todo(id: Annotated[int, Path(title="The ID of the item to get", gt=0)], db_session: db_dependency,
             user_dependency: user_dependency):
    stmt = select(Todos).where(Todos.id == id).where(Todos.user_id == user_dependency.id)
    todo_model = db_session.scalars(stmt)
    todo_model = todo_model.first()
    print(todo_model)
    if todo_model:
        return todo_model
    else:
        raise HTTPException(status_code=404, detail="Todo not found")


@router.post("/todos", status_code=status.HTTP_201_CREATED)
async def create_todo(user_dependency: user_dependency, todo_request: TodoRequest, db_session: db_dependency):
    model_obj: Todos = Todos(**todo_request.model_dump())
    model_obj.user = user_dependency
    db_session.add(model_obj)
    db_session.commit()
    return {"message": "Added Todo"}


@router.put("/todos/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(id: Annotated[int, Path(title="The ID of the item to update", gt=0)],
                      todo_request: TodoRequest,
                      db_session: db_dependency,
                      user_dependency: user_dependency):
    stmt = select(Todos).where(Todos.id == id).where(Todos.user_id == user_dependency.id)
    todo_model = db_session.scalars(stmt)
    todo_model = todo_model.first()

    print(todo_model)
    if todo_model:
        todo_model.title = todo_request.title
        todo_model.description = todo_request.description
        todo_model.priority = todo_request.priority
        todo_model.complete = todo_request.complete
        db_session.commit()
        return todo_model
    else:
        raise HTTPException(status_code=404, detail="Todo not found")


@router.delete(("/todos/{id}"), status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(id: Annotated[int, Path(title="The ID of the item to delete", gt=0)], db_session: db_dependency,
                      user_dependency: user_dependency):
    stmt = select(Todos).where(Todos.id == id).where(Todos.user_id == user_dependency.id)
    todo_model = db_session.scalars(stmt)
    todo_model = todo_model.first()
    if todo_model:
        db_session.delete(todo_model)
        db_session.commit()
    else:
        raise HTTPException(status_code=404, detail="Todo not found")
