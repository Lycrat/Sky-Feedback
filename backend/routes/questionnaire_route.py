from flask import Blueprint, request, jsonify
from backend.services import questionnaire_service

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
    try:
        questionnaires = questionnaire_service.get_questionnaires()
        return jsonify(questionnaires), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@questionnaire_bp.route('/', methods=['POST'])
def add_questionnaire():
    data = request.get_json()
    title = data.get('title')
    if not title:
        return jsonify({"error": "Title is required"}), 400
    
    try:
        new_questionnaire = questionnaire_service.create_questionnaire(title)
        return jsonify(new_questionnaire), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@questionnaire_bp.route('/<int:questionnaire_id>', methods=['GET'])
def get_questionnaire(questionnaire_id):
    try:
        questionnaire = questionnaire_service.get_questionnaire(questionnaire_id)
        return jsonify(questionnaire), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@questionnaire_bp.route('/<int:questionnaire_id>', methods=['PUT'])
def update_questionnaire(questionnaire_id):
    data = request.get_json()
    title = data.get('title')
    if not title:
        return jsonify({"error": "Title is required"}), 400

    try:
        updated_questionnaire = questionnaire_service.update_questionnaire(questionnaire_id, title)
        return jsonify(updated_questionnaire), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@questionnaire_bp.route('/<int:questionnaire_id>', methods=['DELETE'])
def delete_questionnaire(questionnaire_id):
    try:
        questionnaire_service.delete_questionnaire(questionnaire_id)
        return jsonify({"message": "Questionnaire deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500