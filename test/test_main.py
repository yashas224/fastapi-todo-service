"""
TestClient is a testing utility provided by FastAPI (built on top of Starlette's test client).

It allows you to call your API endpoints without starting the actual server using uvicorn

"""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "Todo service healthy"}
