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
        details = data_access.callproc("GETQuestionnaire", (questionnaire_id,))
    except pymysql.MySQLError as e:
        raise RuntimeError(f'Database query error: {e}')

    # Group rows to consolidate options under each question
    questions_map = {}
    for row in details or []:
        qid = row.get('question_id') or row.get('id')
        if not qid:
            continue
        if qid not in questions_map:
            questions_map[qid] = {
                'id': qid,
                'questionnaire_id': questionnaire_id,
                'question': row.get('question'),
                'type': row.get('type', 'text'),
                'options': []
            }
        if row.get('option_text') is not None:
            questions_map[qid]['options'].append(row['option_text'])

    questions_list = list(questions_map.values())
    return {"questionnaire": questionnaire, "questions": questions_list}

#  CREATE questionnaire
def create_questionnaire(data):
    questionnaire_title = data.get('title')
    questions_list = data.get('questions_list') or []

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
            if isinstance(item, dict):
                q_text = item.get('question') or item.get('text') or item.get('title')
                q_type = item.get('type')
                options = item.get('options')
            else:
                q_text = str(item)
                q_type = 'text'
                options = None
            add_question(last_row_id, q_text, q_type or ('multiple' if options else 'text'), options)

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
    # Title can be optional when only questions are being modified
    title = data.get('title')

    # Preferred new contract: provide a full list of questions to sync
    questions_list = data.get('questions_list')
    # Backward compatibility: allow explicit update list
    to_update_ques_list = data.get('to_update_questions')

    data_access = DataAccess()
    if title is not None:
        data_access.callproc('UpdateQuestionnaire', (questionnaire_id, title,))

    # If a full list is provided, sync (add/update/delete) and handle options
    if isinstance(questions_list, list):
        # Fetch current questions
        try:
            from services.question_service import get_questions, delete_question
        except Exception:
            # Local import fallback already available at top for add/update
            from services import question_service as _qs
            get_questions = _qs.get_questions
            delete_question = _qs.delete_question

        current = get_questions(questionnaire_id) or []
        current_ids = {q.get('id') for q in current if q.get('id') is not None}

        provided_ids = set()
        for item in questions_list:
            if isinstance(item, dict):
                qid = item.get('id')
                q_text = item.get('question') or item.get('text') or item.get('title')
                q_type = item.get('type')
                options = item.get('options')
            else:
                qid = None
                q_text = str(item)
                q_type = 'text'
                options = None

            if qid and qid in current_ids:
                provided_ids.add(qid)
                update_question(questionnaire_id, qid, {
                    'question': q_text,
                    'type': q_type,
                    'options': options
                })
            else:
                created = add_question(
                    questionnaire_id,
                    q_text,
                    q_type or ('multiple' if options else 'text'),
                    options
                )
                # Track created id to avoid accidental deletion in subsequent cleanup
                if created and isinstance(created, dict) and created.get('id'):
                    provided_ids.add(created['id'])

        # Delete questions that were removed from the list
        to_delete = current_ids - provided_ids
        for qid in to_delete:
            delete_question(qid)

    # Legacy partial update: only update provided items
    elif to_update_ques_list:
        for item in to_update_ques_list:
            qid = item['id']
            update_question(questionnaire_id, qid, item)

    updated_questionnaire = get_questionnaire(questionnaire_id)

    return updated_questionnaire



