from flask import Blueprint, request, jsonify
from backend.services import questionnaire_service
from backend.services import question_service

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
    
    
# CREATE TABLE Question (
#   id INT AUTO_INCREMENT,
#   questionnaire_id INT NOT NULL,
#   question VARCHAR(200) NOT NULL,
#   PRIMARY KEY (id),
#   FOREIGN KEY (questionnaire_id) REFERENCES Questionnaire (id)
# );
# Use placeholder routes for /questionnaire/<id>/question

# get questions
@questionnaire_bp.route('/<int:questionnaire_id>/question', methods=['GET'])
def get_questions(questionnaire_id):
    try:
        questions = question_service.get_questions(questionnaire_id)
        return jsonify(questions), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@questionnaire_bp.route('/<int:questionnaire_id>/question', methods=['POST'])
def add_question(questionnaire_id):
    data = request.get_json()
    question_text = data.get('question')
    if not question_text:
        return jsonify({"error": "Question text is required"}), 400
    
    try:
        new_question = question_service.add_question(questionnaire_id, question_text)
        return jsonify(new_question), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@questionnaire_bp.route('/<int:questionnaire_id>/question/<int:question_id>', methods=['GET'])
def get_question(questionnaire_id, question_id):
    try:
        question = question_service.get_question(question_id)
        return jsonify(question), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@questionnaire_bp.route('/<int:questionnaire_id>/question/<int:question_id>', methods=['PUT'])
def update_question(questionnaire_id, question_id):
    data = request.get_json()
    question_text = data.get('question')
    if not question_text:
        return jsonify({"error": "Question text is required"}), 400
    
    try:
        updated_question = question_service.update_question(question_id, question_text)
        return jsonify(updated_question), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@questionnaire_bp.route('/<int:questionnaire_id>/question/<int:question_id>', methods=['DELETE'])
def delete_question(questionnaire_id, question_id):
    try:
        question_service.delete_question(question_id)
        return jsonify({"message": "Question deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500