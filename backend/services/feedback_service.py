import pymysql

from database.data_access import DataAccess


#  GET ALL Feedbacks
def get_feedbacks(questionnaire_id):
    data_access = DataAccess()
    try:
        feedbacks = data_access.query("SELECT id, question_id, user_id, feedback FROM Feedback")
    except pymysql.MySQLError as e:
        raise RuntimeError(f'Database query error: {e}')

    # Convert to a dictionary for easier consumption
    return feedbacks

def get_feedbacks_by_user_id(user_id):
    data_access = DataAccess()
    try:
        user_feedbacks = data_access.query("SELECT id, question_id, feedback FROM Feedback WHERE id=%s", user_id)
    except pymysql.MySQLError as e:
        raise RuntimeError(f'Database query error: {e}')

    # Convert to a dictionary for easier consumption
    return user_feedbacks

def get_feedback_by_question_id(question_id):
    data_access = DataAccess()
    try:
        question_feedback = data_access.query("SELECT id, user_id, feedback FROM Feedback WHERE id=%s", question_id)
    except pymysql.MySQLError as e:
        raise RuntimeError(f'Database query error: {e}')

    # Convert to a dictionary for easier consumption
    return question_feedback[0]

#  GET a specific user
def get_feedback(feedback_id):
    data_access = DataAccess()
    try:
        feedback = data_access.query("SELECT id, question_id, user_id, feedback FROM Feedback WHERE id = %s", feedback_id)
    except pymysql.MySQLError as e:
        raise RuntimeError(f'Database query error: {e}')

    # Convert to a dictionary for easier consumption
    return feedback[0]


#  ADD Feedback
def add_feedback(user_id, question_id, feedback):
    try:
        data_access = DataAccess()
        lastrowid = data_access.execute("INSERT INTO User (user_id, question_id, feedback) VALUES (%s, %s, %s);",
                                        (user_id, question_id, feedback))
        feedback = get_feedback(lastrowid)
        return feedback
    except Exception as e:
        raise e


