import pymysql

from database.data_access import DataAccess


#  GET ALL Feedbacks
def get_feedbacks():
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
        user_feedbacks = data_access.query("SELECT id, question_id, feedback FROM Feedback WHERE user_id=%s", user_id)
    except pymysql.MySQLError as e:
        raise RuntimeError(f'Database query error: {e}')

    # Convert to a dictionary for easier consumption
    return user_feedbacks

def get_feedback_by_question_id(question_id):
    data_access = DataAccess()
    try:
        question_feedback = data_access.query("SELECT id, user_id, feedback FROM Feedback WHERE question_id=%s", question_id)
    except pymysql.MySQLError as e:
        raise RuntimeError(f'Database query error: {e}')

    # Convert to a dictionary for easier consumption
    return question_feedback

#  GET feedback by feedback id
def get_feedback(feedback_id):
    data_access = DataAccess()
    try:
        feedback = data_access.query("SELECT id, question_id, user_id, feedback FROM Feedback WHERE id = %s", feedback_id)
    except pymysql.MySQLError as e:
        raise RuntimeError(f'Database query error: {e}')

    # Convert to a dictionary for easier consumption
    return feedback


#  ADD Feedback
def add_feedback(user_id, question_id, feedback):
    try:
        data_access = DataAccess()
        # lastrowid = data_access.execute("INSERT INTO Users (user_id, question_id, feedback) VALUES (%s, %s, %s);",
        #                                 (user_id, question_id, feedback))
        # feedback = get_feedback(lastrowid)
        data_access.callproc("AddFeedback",(question_id,user_id,feedback))
        last_row_id = data_access.get_lastrowid_for_callproc()

        feedback = get_feedback(last_row_id)
        return feedback
    except Exception as e:
        raise e


