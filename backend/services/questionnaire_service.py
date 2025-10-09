import pymysql

from db.data_access import DataAccess
from flask import jsonify


#  GET ALL questionnaires
def questionnaires():
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
        questionnaire = data_access.query("SELECT id, title, created_at FROM Questionnaire WHERE id = %s", (questionnaire_id))
    except pymysql.MySQLError as e:
        raise RuntimeError(f'Database query error: {e}')

    if not result:
        return None

    # Convert to a dictionary for easier consumption
    return result[0]

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
        lastrowid = data_access.execute("INSERT INTO Questionnaire (title) VALUES (%s);",(questionnaire_title))
        questionnaire = get_questionnaire(lastrowid)

        # Now add the questions to the question table
        return jsonify({'title': questionnaire_title}), 201
    except Exception as e:
        raise e

# DELETE questionnaire
def delete_questionnaire(data):
    questionnaire_id = data.get('questionnaire_id')

    if not questionnaire_id:
        return jsonify({'error': 'Questionnaire id is required'}), 400

    try:
        data_access = DataAccess()
        questionnaire = data_access.query("DELETE  FROM Questionnaire WHERE id = (%s);",(questionnaire_id))

        return jsonify({'title': questionnaire_title}), 201
    except Exception as e:
        raise e
        
def update_questionnaire(data):
    # 'id' is required; other fields are optional
    if 'questionnaire_id' not in data:
        raise ValueError("Missing required field: 'questionnaire_id'")

     if 'question_id' not in data:
        raise ValueError("Missing required field: 'question_id'")

    questionnaire_id = data['questionnaire_id']
    set_clauses = []
    params = []

    if 'title' in data:
        set_clauses.append("title = %s")
        params.append(data['title'])

    if not set_clauses:
        raise ValueError("No updatable fields provided")

    params.append(questionnaire_id)
    update_query = f"UPDATE Questionnaire SET {', '.join(set_clauses)} WHERE id = %s"

    dao = DataAccess()
    dao.execute(update_query, params)

    # Update the questions

    # 

    return get_questionnaire(questionnaire_id)




