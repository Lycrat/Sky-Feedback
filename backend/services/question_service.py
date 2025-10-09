import pymysql

from backend.database.data_access import DataAccess
from flask import jsonify

#  GET ALL questions of a specific questionnaires
def get_questions (questionnaire_id):
    data_access = DataAccess()
    try:
        questions = data_access.query("SELECT id, questionnaire_id, question FROM Question WHERE id = %s", questionnaire_id)
    except pymysql.MySQLError as e:
        raise RuntimeError(f'Database query error: {e}')

    # Convert to a dictionary for easier consumption
    return questions

#  GET a specific question
def get_question (question_id):

    data_access = DataAccess()
    try:
        question = data_access.query("SELECT id, questionnaire_id, question FROM Question WHERE id = %s", question_id)
    except pymysql.MySQLError as e:
        raise RuntimeError(f'Database query error: {e}')

    # Convert to a dictionary for easier consumption
    return question


#  ADD question
def add_question(questionnaire_id, data):

    question = data.get('question')
    try:
        data_access = DataAccess()
        lastrowid = data_access.execute("INSERT INTO Question (question, questionnaire_id) VALUES (%s, %s);",(question, questionnaire_id))
        question = get_question(lastrowid)

        # Now add the questions to the question table
        return jsonify({'question': question}), 201
    except Exception as e:
        raise e

# DELETE question
def delete_question(question_id):
    try:
        data_access = DataAccess()
        rowid = data_access.execute("DELETE FROM Question WHERE id = (%s);", question_id)
        question = get_question(rowid)

        return jsonify({'question': question}), 201
    except Exception as e:
        raise e
        
def update_question(question_id, data):

    if 'question' not in data:
        raise ValueError("Missing required field: 'question'")

    question = data['question']

    data_access = DataAccess()
    rowid = data_access.execute("UPDATE Question SET question=(%s) WHERE id = (%s);",(question, question_id))
    question = get_question(rowid)

    return question




