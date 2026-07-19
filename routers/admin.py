from typing import Annotated

from fastapi import APIRouter
from fastapi import HTTPException, status, Path, Depends
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import select
from models import Users
from routers.auth import get_current_user
from dependencies import db_dependency
from models import Todos

user_dependency = Annotated[Users, Depends(get_current_user)]


def is_admin_check(user_dependency: user_dependency):
    if user_dependency.role == "admin":
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation Not Allowed"
        )


router = APIRouter(dependencies=[Depends(is_admin_check)], prefix="/admin", tags=["admin"])


@router.get("/todos")
async def read_all(db_session: db_dependency):
    return db_session.scalars(select(Todos)).all()


@router.delete(("/todos/{id}"), status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(id: Annotated[int, Path(title="The ID of the item to delete", gt=0)], db_session: db_dependency):
    stmt = select(Todos).where(Todos.id == id)
    todo_model = db_session.scalars(stmt)
    todo_model = todo_model.first()
    if todo_model:
        db_session.delete(todo_model)
        db_session.commit()
    else:
        raise HTTPException(status_code=404, detail="Todo not found")
