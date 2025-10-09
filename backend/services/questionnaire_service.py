import pymysql

from backend.database.data_access import DataAccess
from backend.services.question_service import add_question
from flask import jsonify


#  GET ALL questionnaires
def get_questionnaires():
    try:
        data_access = DataAccess()
        questionnaires = data_access.query("SELECT id, title, created_at FROM Questionnaire ORDER BY created_at DESC;")
        return questionnaires
    except Exception as e:
        raise e

#  GET a specific questionnaires
def get_questionnaire (questionnaire_id):
    data_access = DataAccess()
    try:
        questionnaire = data_access.query("SELECT id, title, created_at FROM Questionnaire WHERE id = %s", questionnaire_id)
    #      To add a stored procedure to return all the questions of the questionnaire as well

    except pymysql.MySQLError as e:
        raise RuntimeError(f'Database query error: {e}')

    if not questionnaire:
        return None

    # Convert to a dictionary for easier consumption
    return questionnaire[0]

#  CREATE questionnaire
def create_questionnaire(data):
    questionnaire_title = data.get('title')
    questions_list = data.get('questions_list')

    if not questionnaire_title:
        return jsonify({'error': 'Questionnaire title is required'}), 400

    if not questions_list:
        return jsonify({'error': 'Questions list is required'}), 400

    try:
        data_access = DataAccess()
        lastrowid = data_access.execute("INSERT INTO Questionnaire (title) VALUES (%s);",questionnaire_title)
        questionnaire = get_questionnaire(lastrowid)

        # Add the questions to the question table
        for item in questions_list:
            add_question(lastrowid, item)

        return jsonify({'questionnaire': questionnaire}), 201
    except Exception as e:
        raise e

# DELETE questionnaire
def delete_questionnaire(data):
    questionnaire_id = data.get('questionnaire_id')

    if not questionnaire_id:
        return jsonify({'error': 'Questionnaire id is required'}), 400

    try:
        data_access = DataAccess()
        questionnaire = data_access.execute("DELETE FROM Questionnaire WHERE id = (%s);",questionnaire_id)

        return jsonify({'title': questionnaire}), 201
    except Exception as e:
        raise e

def update_questionnaire(data):
    if 'questionnaire_id' not in data:
        raise ValueError("Missing required field: 'questionnaire_id'")

    if 'question_id' not in data:
        raise ValueError("Missing required field: 'question_id'")

    questionnaire_id = data['questionnaire_id']
    title = data['title']
    to_update_ques_list = data['update_questions']

    data_access = DataAccess()
    update_query = data_access.execute("UPDATE Questionnaire SET title= (%s) WHERE id = (%s);",(title, questionnaire_id))

    # Update the questions in the question table
    for item in to_update_ques_list:
        update_question(lastrowid, item)

    return get_questionnaire(questionnaire_id)




