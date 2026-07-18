from fastapi import APIRouter, status
from pydantic import BaseModel, Field
from models import Users
from dependencies import db_dependency
from utils import password_util

router = APIRouter()


class CreateUserRequest(BaseModel):
    username: str = Field()
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(create_user_req: CreateUserRequest
                      , db_session: db_dependency):
    user_model: Users = Users(
        username=create_user_req.username,
        email=create_user_req.email,
        first_name=create_user_req.first_name,
        last_name=create_user_req.last_name,
        hashed_password=password_util.hash_password(create_user_req.password),
        role=create_user_req.role,
        is_active=True
    )
    db_session.add(user_model)
    db_session.commit()
    return {"message": "User Created "}
