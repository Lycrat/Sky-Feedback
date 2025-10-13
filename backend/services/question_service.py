import pymysql

from database.data_access import DataAccess

# Helpers for options
def get_options_by_question_id(question_id):
    data_access = DataAccess()
    try:
        rows = data_access.query("SELECT id, option_text FROM Options WHERE question_id = %s ORDER BY id ASC", question_id)
        return rows
    except pymysql.MySQLError as e:
        raise RuntimeError(f'Database query error: {e}')

def add_option(question_id, option_text):
    data_access = DataAccess()
    try:
        data_access.callproc("AddOption", (question_id, option_text))
    except pymysql.MySQLError as e:
        raise RuntimeError(f'Database query error: {e}')

def replace_options(question_id, options):
    data_access = DataAccess()
    try:
        data_access.callproc("DeleteOptionsForQuestion", (question_id,))
        for opt in options or []:
            if opt is not None and str(opt).strip() != "":
                add_option(question_id, opt)
    except Exception as e:
        raise e


#  GET ALL questions of a specific questionnaires
def get_questions (questionnaire_id):
    data_access = DataAccess()
    try:
        questions = data_access.query("SELECT id, questionnaire_id, question, type FROM Question WHERE questionnaire_id = %s", questionnaire_id)
    except pymysql.MySQLError as e:
        raise RuntimeError(f'Database query error: {e}')

    return questions

#  GET a specific question
def get_question (question_id):
    data_access = DataAccess()
    try:
        rows = data_access.query("SELECT id, questionnaire_id, question, type FROM Question WHERE id = %s", question_id)
        if isinstance(rows, list):
            base = rows[0] if rows else None
        else:
            base = rows
        if not base:
            return None
        opts = get_options_by_question_id(base['id'])
        base['options'] = [o['option_text'] for o in opts] if isinstance(opts, list) else []
        return base
    except pymysql.MySQLError as e:
        raise RuntimeError(f'Database query error: {e}')


#  ADD question
def add_question(questionnaire_id, question, q_type='text', options=None):
    try:
        data_access = DataAccess()
        data_access.callproc("AddQuestion", (questionnaire_id, question, q_type))
        last_row_id = data_access.get_lastrowid_for_callproc()

        # Add options if provided
        if options:
            for opt in options:
                if opt is not None and str(opt).strip() != "":
                    add_option(last_row_id, opt)

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
    q_type = data.get('type')
    options = data.get('options')
    data_access = DataAccess()

    # Keep existing type if not provided
    if not q_type:
        current = get_question(question_id)
        q_type = current['type'] if current else 'text'

    data_access.callproc("UpdateQuestion", (questionnaire_id, question_id, question, q_type))

    # Replace options for multiple choice; clear if not multiple
    if q_type == 'multiple':
        replace_options(question_id, options or [])
    else:
        replace_options(question_id, [])

    updated_question = get_question(question_id)

    return updated_question




