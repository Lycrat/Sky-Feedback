import pymysql

from backend.database.data_access import DataAccess
from backend.services.question_service import add_question, update_question

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
        details = data_access.query("CALL GETQuestionnaire(%s);", questionnaire_id)
    except pymysql.MySQLError as e:
        raise RuntimeError(f'Database query error: {e}')

    return {"questionnaire": questionnaire, "questions": details}

#  CREATE questionnaire
def create_questionnaire(data):
    questionnaire_title = data.get('title')
    questions_list = data.get('questions_list')

    try:
        data_access = DataAccess()
        data_access.execute("CALL AddQuestionnaire (%s);", questionnaire_title)

        # Retrieve the newly created questionnaire
        questionnaire = data_access.query("SELECT id, title, created_at FROM Questionnaire WHERE title = %s ORDER BY created_at DESC LIMIT 1;", questionnaire_title)

        lastrowid = questionnaire[0]['id']

        # Add the questions to the question table
        for item in questions_list:
            add_question(lastrowid, item)

        questionnaire = get_questionnaire(lastrowid)

        return questionnaire
    except Exception as e:
        raise e

# DELETE questionnaire
def delete_questionnaire(data):
    questionnaire_id = data.get('questionnaire_id')

    try:
        data_access = DataAccess()
        data_access.execute("DELETE FROM Questionnaire WHERE id = (%s);", questionnaire_id)

        return True
    except Exception as e:
        raise e

def update_questionnaire(data):
    questionnaire_id = data['questionnaire_id']
    title = data['title']
    to_update_ques_list = data['update_questions']

    data_access = DataAccess()
    lastrowid = data_access.execute("CALL UpdateQuestionnaire(%s , %s);",(questionnaire_id, title))
    updated_questionnaire = get_questionnaire(lastrowid)

    # Update the questions in the question table
    for item in to_update_ques_list:
        update_question(item['id'], item)

    return updated_questionnaire




