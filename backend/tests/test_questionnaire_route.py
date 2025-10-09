import flask
import pytest
from app import create_app

app = create_app()

# Make app a proper pytest fixture
@pytest.fixture
def app():
    return create_app()

@pytest.fixture
def client(app):
    return app.test_client()

# CREATE TABLE Questionnaire (
#   id INT AUTO_INCREMENT,
#   title VARCHAR(100) NOT NULL,
#   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#   PRIMARY KEY (id)
# );

# test questionnaire routes

def test_get_questionnaires():
    response = app.test_client().get('/api/questionnaire/')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]['title'] == "Customer Satisfaction"
    assert data[1]['title'] == "Product Feedback"

