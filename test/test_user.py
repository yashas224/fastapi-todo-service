from fastapi.testclient import TestClient

from dependencies import get_db_session
from main import app
from routers.users import get_current_user

from test.test_database import override_get_db_session, override_get_current_user, load_db

client = TestClient(app)

app.dependency_overrides[get_db_session] = override_get_db_session
app.dependency_overrides[get_current_user] = override_get_current_user


def test_get_user_details(load_db):
    response = client.get("/user")
    assert response.status_code == 200
    print(response.json())
    assert response.json() == {
        "username": "john_doe",
        "email": "john.doe@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "role": "admin",
    }


def test_password_change(load_db):
    response = client.put(
        "user/update/password",
        json={
            "currentPassword": "test12",
            "newPassword": "test12345",
        }
    )
    assert response.status_code == 204


def test_password_change_invalid(load_db):
    response = client.put(
        "user/update/password",
        json={
            "currentPassword": "test12invalid",
            "newPassword": "test12345",
        }
    )
    assert response.status_code == 401
