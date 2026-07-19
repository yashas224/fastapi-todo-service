from fastapi.testclient import TestClient
from dependencies import get_db_session
from main import app
from routers.todos import get_current_user
from test.test_database import load_db, override_sessionLocal
from sqlalchemy import select
from models import Todos
from test.test_database import override_get_db_session, override_get_current_user

client = TestClient(app)

app.dependency_overrides[get_db_session] = override_get_db_session
app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_all(load_db):
    response = client.get("/todos")
    assert response.status_code == 200
    print(response.json())
    assert response.json() == [{
        "id": 1,
        "user_id": 1,
        "title": "Learn to code!",
        "description": "Need to learn everyday!",
        "priority": 5,
        "complete": False,
    }]


def test_read_one_exists(load_db):
    response = client.get("/todos/1")
    assert response.status_code == 200
    print(response.json())
    assert response.json() == {
        "id": 1,
        "user_id": 1,
        "title": "Learn to code!",
        "description": "Need to learn everyday!",
        "priority": 5,
        "complete": False,
    }


def test_read_one__not_exists(load_db):
    response = client.get("/todos/2")
    assert response.status_code == 404
    print(response.json())
    assert response.json() == {'detail': 'Todo not found'}


def test_create_todo(load_db):
    response = client.post(
        "/todos/",
        json={
            "title": "leisure Time!",
            "description": "Play a sport",
            "priority": 5,
            "complete": False,
        }
    )
    assert response.status_code == 201
    assert response.json() == {"message": "Added Todo"}

    session = override_sessionLocal()
    saved_obj = session.scalars(select(Todos).where(Todos.id == 2)).first()
    assert saved_obj is not None
    assert saved_obj.title == "leisure Time!"


def test_update_todo(load_db):
    response = client.put(
        "/todos/1",
        json={
            "title": "Learn to code!",
            "description": "Need to learn everyday!",
            "priority": 5,
            "complete": True,
        }
    )
    assert response.status_code == 204

    session = override_sessionLocal()
    saved_obj = session.scalars(select(Todos).where(Todos.id == 1)).first()
    assert saved_obj is not None
    assert saved_obj.complete is True


def test_update_todo_no_found(load_db):
    response = client.put(
        "/todos/2",
        json={
            "title": "Learn to code!",
            "description": "Need to learn everyday!",
            "priority": 5,
            "complete": True,
        }
    )
    assert response.status_code == 404


def test_delete_todo(load_db):
    response = client.delete(
        "/todos/1")
    assert response.status_code == 204

    session = override_sessionLocal()
    saved_obj = session.scalars(select(Todos).where(Todos.id == 1)).first()
    assert saved_obj is None
