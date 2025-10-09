from flask import Blueprint, request, jsonify

# prefix with /api
questionnaire_bp = Blueprint('questionnaire', __name__, url_prefix='/api/questionnaire')

# CREATE TABLE Questionnaire (
#   id INT AUTO_INCREMENT,
#   title VARCHAR(100) NOT NULL,
#   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#   PRIMARY KEY (id)
# );

@questionnaire_bp.route('/', methods=['GET'])
def get_questionnaires():
    # Placeholder for fetching questionnaires from the database
    questionnaires = [
        {"id": 1, "title": "Customer Satisfaction"},
        {"id": 2, "title": "Product Feedback"}
    ]
    return jsonify(questionnaires)