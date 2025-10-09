import pytest

from backend.app import create_app

@pytest.fixture
def app():
    return create_app()

@pytest.fixture
def client(app):
    return app.test_client()

# ---- MOCK FUNCTIONS ----
@pytest.fixture
def mock_services(monkeypatch):

    # CREATE TABLE Question (
    #   id INT AUTO_INCREMENT,
    #   questionnaire_id INT NOT NULL,
    #   question VARCHAR(200) NOT NULL,
    #   PRIMARY KEY (id),
    #   FOREIGN KEY (questionnaire_id) REFERENCES Questionnaire (id)
    # );
    # Use placeholder routes for /questionnaire/<id>/question
    # Mock all functions from question_service
    def mock_get_questions(questionnaire_id):
        return [
            {"id": 1, "questionnaire_id": questionnaire_id, "question": "How satisfied are you with our service?"},
            {"id": 2, "questionnaire_id": questionnaire_id, "question": "Would you recommend us to others?"},
        ]
    
    def mock_get_question_by_id(question_id):
        return {"id": question_id, "questionnaire_id": 1, "question": "Mocked Question"}
    
    def mock_add_question(questionnaire_id, question):
        return {"id": 99, "questionnaire_id": questionnaire_id, "question": question}
    
    def mock_update_question(question_id, question):
        return {"id": question_id, "questionnaire_id": 1, "question": question}
    
    def mock_delete_question(question_id):
        return {"message": "Question deleted successfully"}
    
    # Apply monkeypatches
    import backend.services.question_service as service
    monkeypatch.setattr(service, "get_questions", mock_get_questions)
    monkeypatch.setattr(service, "get_question", mock_get_question_by_id)
    monkeypatch.setattr(service, "add_question", mock_add_question)
    monkeypatch.setattr(service, "update_question", mock_update_question)
    monkeypatch.setattr(service, "delete_question", mock_delete_question)

# ---- TESTS ----

def test_get_questions(client, mock_services):
    response = client.get("/api/questionnaire/1/question")
    assert response.status_code == 200
    assert isinstance(response.json, list)
    for question in response.json:
        assert "id" in question
        assert "questionnaire_id" in question
        assert "question" in question

def test_get_question_by_id(client, mock_services):
    response = client.get("/api/questionnaire/1/question/1")
    assert response.status_code == 200
    assert "id" in response.json
    assert "questionnaire_id" in response.json
    assert "question" in response.json

def test_add_question(client, mock_services):
    response = client.post("/api/questionnaire/1/question", json={"question": "Is this a new question?"})
    assert response.status_code == 201
    assert "id" in response.json
    assert response.json["questionnaire_id"] == 1
    assert response.json["question"] == "Is this a new question?"

def test_update_question(client, mock_services):
    response = client.put("/api/questionnaire/1/question/1", json={"question": "Updated question text"})
    assert response.status_code == 200
    assert "id" in response.json
    assert response.json["id"] == 1
    assert response.json["questionnaire_id"] == 1
    assert response.json["question"] == "Updated question text"

def test_delete_question(client, mock_services):
    response = client.delete("/api/questionnaire/1/question/1")
    assert response.status_code == 200
    assert response.json["message"] == "Question deleted successfully"

