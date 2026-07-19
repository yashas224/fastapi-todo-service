import pytest
from sqlalchemy import create_engine
from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

import models
from models import Todos, Users

TEST_SQL_ALCHEMY_DATABASE_URL = "sqlite:///./testDB.db"
testing_engine = create_engine(TEST_SQL_ALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False, "timeout": 30},
                               echo=True)

override_sessionLocal = sessionmaker(bind=testing_engine, autoflush=False, autocommit=False)

models.Base.metadata.create_all(testing_engine)


def override_get_db_session():
    test_db = override_sessionLocal()
    try:
        yield test_db
    finally:
        test_db.close()


def override_get_current_user() -> Users:
    session = override_sessionLocal()
    print("inside override_get_current_user, Fetching user")
    stmt = select(Users).where(Users.id == 1)
    user = session.scalars(stmt).first()
    session.close()
    return user


@pytest.fixture
def load_db():
    print("Adding TODOS")
    todo = Todos(
        title="Learn to code!",
        description="Need to learn everyday!",
        priority=5,
        complete=False,
    )

    user = Users(
        id=1,
        username="john_doe",
        email="john.doe@example.com",
        first_name="John",
        last_name="Doe",
        is_active=True,
        role="user",
        hashed_password="test_hashed_password",
    )
    todo.user = user

    session = override_sessionLocal()
    session.add(todo)
    session.commit()

    yield todo
    stmt = delete(Todos)
    session.execute(stmt)
    stmt = delete(Users)
    session.execute(stmt)
    session.commit()
    session.close()

    print("Closing database")
