from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_list_users_empty():
    resp = client.get("/api/v1/users")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
