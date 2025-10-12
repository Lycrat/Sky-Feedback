import pytest
from app import create_app

@pytest.fixture
def app():
    return create_app()

@pytest.fixture
def client(app):
    return app.test_client()

# ---- MOCK FUNCTIONS ----
@pytest.fixture
def mock_services(monkeypatch):
    """Mock all functions from questionnaire_service."""

    # Mock get_all_questionnaires
    def mock_get_all_questionnaires():
        return [
            {"id": 1, "title": "Customer Satisfaction", "created_at": "2024-01-01T00:00:00"},
            {"id": 2, "title": "Product Feedback", "created_at": "2024-01-01T00:00:00"},
        ]

    # Mock get_questionnaire_by_id
    def mock_get_questionnaire_by_id(questionnaire_id):
        # return a questionnaire and questions as well
        return {
            "id": questionnaire_id,
            "title": "Mocked Questionnaire",
            "created_at": "2024-01-01T00:00:00",
            "questions": [
                {"id": 1, "questionnaire_id": questionnaire_id, "question": "How satisfied are you with our service?"},
                {"id": 2, "questionnaire_id": questionnaire_id, "question": "Would you recommend us to others?"},
            ]
        }
    
    # Mock add_questionnaire
    def mock_add_questionnaire(title):
        return {"id": 99, "title": title, "created_at": "2024-01-01T00:00:00"}

    # Mock update_questionnaire
    def mock_update_questionnaire(questionnaire_id, title):
        return {"id": questionnaire_id, "title": title, "created_at": "2024-01-01T00:00:00"}

    # Mock delete_questionnaire
    def mock_delete_questionnaire(questionnaire_id):
        return True

    # Apply monkeypatches
    import backend.services.questionnaire_service as service
    monkeypatch.setattr(service, "get_questionnaires", mock_get_all_questionnaires)
    monkeypatch.setattr(service, "get_questionnaire", mock_get_questionnaire_by_id)
    monkeypatch.setattr(service, "create_questionnaire", mock_add_questionnaire)
    monkeypatch.setattr(service, "update_questionnaire", mock_update_questionnaire)
    monkeypatch.setattr(service, "delete_questionnaire", mock_delete_questionnaire)


# ---- TESTS ----

def test_get_questionnaires(client, mock_services):
    response = client.get("/api/questionnaire/")
    assert response.status_code == 200
    assert isinstance(response.json, list)
    for questionnaire in response.json:
        assert "id" in questionnaire
        assert "title" in questionnaire
        assert "created_at" in questionnaire

def test_get_questionnaire(client, mock_services):
    response = client.get("/api/questionnaire/1")
    assert response.status_code == 200
    assert "id" in response.json
    assert response.json["id"] == 1
    assert "title" in response.json
    assert "created_at" in response.json
    assert "questions" in response.json
    assert isinstance(response.json["questions"], list)
    for question in response.json["questions"]:
        assert "id" in question
        assert "questionnaire_id" in question
        assert question["questionnaire_id"] == 1
        assert "question" in question


def test_add_questionnaire(client, mock_services):
    new_questionnaire = {"title": "New Questionnaire"}
    response = client.post("/api/questionnaire/", json=new_questionnaire)
    assert response.status_code == 201
    assert "id" in response.json
    assert response.json["title"] == new_questionnaire["title"]
    assert "created_at" in response.json


def test_delete_questionnaire(client, mock_services):
    # Add one to delete (mocked id = 99)
    new_questionnaire = {"title": "To Delete"}
    post_response = client.post("/api/questionnaire/", json=new_questionnaire)
    assert post_response.status_code == 201
    questionnaire_id = post_response.json["id"]

    delete_response = client.delete(f"/api/questionnaire/{questionnaire_id}")
    assert delete_response.status_code == 200
    assert delete_response.json["message"] == "Questionnaire deleted successfully"


def test_update_questionnaire(client, mock_services):
    # Add one to update
    new_questionnaire = {"title": "To Update"}
    post_response = client.post("/api/questionnaire/", json=new_questionnaire)
    assert post_response.status_code == 201
    questionnaire_id = post_response.json["id"]

    updated_data = {"title": "Updated Title"}
    put_response = client.put(f"/api/questionnaire/{questionnaire_id}", json=updated_data)
    assert put_response.status_code == 200
    assert put_response.json["id"] == questionnaire_id
    assert put_response.json["title"] == updated_data["title"]
