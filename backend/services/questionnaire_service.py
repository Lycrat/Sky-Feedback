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
    questions_list = data.get('questions_list', [])

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
            # split question and options if any
            question_text = item.get('question')
            question_options = item.get('options', [])
            question_type = "text" if not question_options else "multiple-choice"

            add_question(last_row_id, question_text, question_options, question_type)

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
    # get new questions list (with new, updated and deleted questions)
    new_ques_list = data.get('questions_list', [])
    # get current questions list from db
    current_ques_list = get_questionnaire(questionnaire_id).get('questions', [])

    # Determine which questions to add, update, or delete
    current_ques_dict = {q['id']: q for q in current_ques_list}
    existing_updated_ques_dict = {q.get('id'): q for q in new_ques_list if q.get('id') is not None}

    # Questions to delete (present in current but not in new)
    to_delete = [q_id for q_id in current_ques_dict if q_id not in existing_updated_ques_dict]
    # Questions to add (present in new but not in current)
    to_add = [q for q in new_ques_list if q.get('id') is None]
    # Questions to update (present in both)
    to_update = [existing_updated_ques_dict[q_id] for q_id in existing_updated_ques_dict if q_id in current_ques_dict]


    updated_questionnaire = get_questionnaire(questionnaire_id)

    return updated_questionnaire




