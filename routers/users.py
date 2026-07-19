from typing import Annotated

from fastapi import APIRouter
from fastapi import status, Depends
from pydantic import BaseModel, Field
from sqlalchemy import select

from dependencies import db_dependency
from models import Users
from routers.auth import get_current_user
from utils import password_util

router = APIRouter(dependencies=[Depends(get_current_user)], prefix="/user", tags=["user"])
user_dependency = Annotated[Users, Depends(get_current_user)]


class UserResponse(BaseModel):
    first_name: str
    last_name: str
    email: str
    username: str
    role: str


class UpdatePassword(BaseModel):
    password: str = Field(max_length=30, min_length=5)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user_details(current_user: user_dependency, db_session: db_dependency):
    model: Users = db_session.scalars(select(Users).where(Users.id == current_user.id)).first()
    return UserResponse(
        first_name=model.first_name,
        last_name=model.last_name,
        email=model.email,
        username=model.username,
        role=model.role
    )


@router.put("/update/password", status_code=status.HTTP_204_NO_CONTENT)
async def update_password(req_obj: UpdatePassword, db_session: db_dependency, current_user: user_dependency):
    current_user.hashed_password = password_util.hash_password(req_obj.password)
    db_session.commit()
