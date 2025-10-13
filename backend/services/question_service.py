import pymysql

from database.data_access import DataAccess

#  GET ALL questions of a specific questionnaires
def get_questions (questionnaire_id):
    data_access = DataAccess()
    try:
        questions = data_access.query("SELECT id, questionnaire_id, question FROM Question WHERE questionnaire_id = %s", questionnaire_id)
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
def add_question(questionnaire_id, question):
    try:
        data_access = DataAccess()
        # data_access.execute("CALL AddQuestion(%s, %s);",(questionnaire_id, question))

        # # Retrieve the newly created question
        # question = data_access.query("SELECT id FROM Question WHERE question = %s AND questionnaire_id = %s ORDER BY id DESC LIMIT 1;", (question, questionnaire_id))

        data_access.callproc("AddQuestion", (questionnaire_id, question))
        last_row_id = data_access.get_lastrowid_for_callproc()

        # Now add the questions to the question table
        return get_question(last_row_id)
    except Exception as e:
        raise e

# DELETE question
def delete_question(question_id):
    try:
        data_access = DataAccess()
        data_access.execute("DELETE FROM Question WHERE id = (%s);", question_id)
        return True
    except Exception as e:
        raise e

# UPDATE question
def update_question(questionnaire_id, question_id, data):
    question = data.get('question')
    data_access = DataAccess()

    data_access.callproc("UpdateQuestion", (questionnaire_id, question_id, question))
    updated_question = get_question(question_id)

    return updated_question




