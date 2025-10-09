import pytest
from app import create_app

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
# get questionaires

def test_get_questionnaires(client):
    response = client.get('/api/questionnaire/')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    for questionnaire in response.json:
        assert 'id' in questionnaire
        assert 'title' in questionnaire
        assert 'created_at' in questionnaire

#  test add questionnaire
def test_add_questionnaire(client):
    new_questionnaire = {
        'title': 'New Questionnaire'
    }
    response = client.post('/api/questionnaire/', json=new_questionnaire)
    assert response.status_code == 201
    assert 'id' in response.json
    assert response.json['title'] == new_questionnaire['title']
    assert 'created_at' in response.json

# test delete questionnaire
def test_delete_questionnaire(client):
    # First, add a questionnaire to delete
    new_questionnaire = {
        'title': 'Questionnaire to Delete'
    }
    post_response = client.post('/api/questionnaire/', json=new_questionnaire)
    assert post_response.status_code == 201
    questionnaire_id = post_response.json['id']

    # Now, delete the questionnaire
    delete_response = client.delete(f'/api/questionnaire/{questionnaire_id}')
    assert delete_response.status_code == 200
    assert delete_response.json['message'] == 'Questionnaire deleted successfully'

    # Verify it's deleted
    get_response = client.get('/api/questionnaire/')
    assert get_response.status_code == 200
    ids = [q['id'] for q in get_response.json]
    assert questionnaire_id not in ids

#  test update questionnaire
def test_update_questionnaire(client):
    # First, add a questionnaire to update
    new_questionnaire = {
        'title': 'Questionnaire to Update'
    }
    post_response = client.post('/api/questionnaire/', json=new_questionnaire)
    assert post_response.status_code == 201
    questionnaire_id = post_response.json['id']

    # Now, update the questionnaire
    updated_data = {
        'title': 'Updated Questionnaire Title'
    }
    put_response = client.put(f'/api/questionnaire/{questionnaire_id}', json=updated_data)
    assert put_response.status_code == 200
    assert put_response.json['id'] == questionnaire_id
    assert put_response.json['title'] == updated_data['title']

    # Verify the update
    get_response = client.get('/api/questionnaire/')
    assert get_response.status_code == 200
    titles = [q['title'] for q in get_response.json if q['id'] == questionnaire_id]
    assert titles[0] == updated_data['title']

