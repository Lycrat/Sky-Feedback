import pymysql

from database.data_access import DataAccess
from services.question_service import add_question, update_question

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
        # To add a stored procedure to return all the questions of the questionnaire as well
        # details = data_access.query("CALL GETQuestionnaire(%s);", questionnaire_id)
        details = data_access.callproc("GETQuestionnaire", (questionnaire_id,))
    except pymysql.MySQLError as e:
        raise RuntimeError(f'Database query error: {e}')

    return {"questionnaire": questionnaire, "questions": details}

#  CREATE questionnaire
def create_questionnaire(data):
    questionnaire_title = data.get('title')
    questions_list = data.get('questions_list')

    try:
        data_access = DataAccess()
        # Use the stored procedure to add the questionnaire and get the last inserted 
        data_access.callproc('AddQuestionnaire', (questionnaire_title,))
        last_row_id = data_access.get_lastrowid_for_callproc()

        # # Retrieve the newly created questionnaire
        # questionnaire = data_access.query("SELECT id, title, created_at FROM Questionnaire WHERE title = %s ORDER BY created_at DESC LIMIT 1;", questionnaire_title)

        # lastrowid = questionnaire[0]['id']

        # Add the questions to the question table
        for item in questions_list:
            add_question(last_row_id, item)

        questionnaire = get_questionnaire(last_row_id)

        return questionnaire
    except Exception as e:
        raise e

# DELETE questionnaire
def delete_questionnaire(questionnaire_id):
    try:
        data_access = DataAccess()
        data_access.execute("DELETE FROM Questionnaire WHERE id = %s;", questionnaire_id)

        return True
    except Exception as e:
        raise e

# UPDATE questionnaire
def update_questionnaire(questionnaire_id, data):

    title = data['title']
    to_update_ques_list = data['to_update_questions']

    data_access = DataAccess()
    data_access.callproc('UpdateQuestionnaire', (questionnaire_id, title,))

    # Update the questions in the question table
    if to_update_ques_list:
        for item in to_update_ques_list:
            update_question(item['id'], item)

    updated_questionnaire = get_questionnaire(questionnaire_id)

    return updated_questionnaire




