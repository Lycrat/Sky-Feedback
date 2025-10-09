import pytest

from backend.app import create_app
from backend.services import user_service

@pytest.fixture
def app():
    return create_app()

@pytest.fixture
def client(app):
    return app.test_client()

# CREATE TABLE User (
#   id INT AUTO_INCREMENT,
#   username VARCHAR(100) NOT NULL,
#   name VARCHAR(100) NOT NULL,
#   PRIMARY KEY (id)
# );

# ---- MOCK FUNCTIONS ----
@pytest.fixture
def mock_services(monkeypatch):
    
    def mock_create_user(data):
        return {"id": 1, "name": data["name"], "username": data["username"]}
    
    def mock_get_user(user_id):
        if user_id == 1:
            return {"id": 1, "name": "John Doe", "username": "johndoe"}
        return None
    
    # Apply monkeypatches
    monkeypatch.setattr(user_service, "create_user", mock_create_user)
    monkeypatch.setattr(user_service, "get_user", mock_get_user)

# ---- TESTS ----
def test_create_user(client, mock_services):
    response = client.post("/api/user/", json={"username": "johndoe", "name": "John Doe"})
    assert response.status_code == 201
    assert response.json["username"] == "johndoe"
    assert response.json["name"] == "John Doe"

def test_create_user_missing_fields(client, mock_services):
    response = client.post("/api/user/", json={"username": "johndoe"})
    assert response.status_code == 400
    assert "error" in response.json
    assert response.json["error"] == "Username and email are required"

def test_get_user(client, mock_services):
    response = client.get("/api/user/1")
    assert response.status_code == 200
    assert response.json["id"] == 1
    assert response.json["username"] == "johndoe"
    assert response.json["name"] == "John Doe"

def test_get_user_not_found(client, mock_services):
    response = client.get("/api/user/999")
    assert response.status_code == 404
    assert "error" in response.json
    assert response.json["error"] == "User not found"


