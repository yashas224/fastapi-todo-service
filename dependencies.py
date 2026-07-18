from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session
from database import sessionLocal


def get_db_session():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db_session)]
