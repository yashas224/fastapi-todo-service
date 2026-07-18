from typing import Annotated
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel, Field
from sqlalchemy import select
import jwt
import os
from dependencies import db_dependency
from models import Users
from utils import password_util

router = APIRouter(
    prefix="/auth"
    , tags=["auth"]
)

load_dotenv()

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = os.getenv("SECRET_KEY")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


class CreateUserRequest(BaseModel):
    username: str = Field()
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db_session: db_dependency):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        print(f"Logged in user: {username}  ")
        stmt = select(Users).where(Users.username == username)
        user: Users = db_session.scalars((stmt)).first()
        if user:
            return user
        else:
            raise
    except:
        HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def authenticate_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
                      , db_session: db_dependency):
    username = form_data.username
    password = form_data.password
    stmt = select(Users).where(Users.username == username)
    user: Users = db_session.scalars((stmt)).first()
    if user:
        is_valid_password = password_util.verify_password(password, user.hashed_password)
        if is_valid_password:
            return user
    else:
        return None

    return None


@router.post("/", status_code=status.HTTP_201_CREATED)
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


@router.post("/token", response_model=Token, status_code=status.HTTP_200_OK, summary="Generate JWT token")
async def get_token(authenticate_user: Annotated[Users, Depends(authenticate_user)]):
    if authenticate_user:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": authenticate_user.username, "id": authenticate_user.id}, expires_delta=access_token_expires
        )
        return Token(
            access_token=access_token,
            token_type="bearer"
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
