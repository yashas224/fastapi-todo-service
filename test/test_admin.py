from main import app
from fastapi.testclient import TestClient
from test.test_database import override_get_db_session, override_get_current_user, load_db
from routers.admin import get_current_user
from dependencies import get_db_session

client = TestClient(app)

app.dependency_overrides[get_db_session] = override_get_db_session
app.dependency_overrides[get_current_user] = override_get_current_user


def test_admin_read_all(load_db):
    response = client.get("/admin/todos")
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
