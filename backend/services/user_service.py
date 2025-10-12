import pymysql

from backend.database.data_access import DataAccess

#  GET ALL Users
def get_users():
    data_access = DataAccess()
    try:
        users = data_access.query("SELECT id, username, name FROM User")
    except pymysql.MySQLError as e:
        raise RuntimeError(f'Database query error: {e}')

    # Convert to a dictionary for easier consumption
    return users


#  GET a specific user
def get_user(user_id):
    data_access = DataAccess()
    try:
        user = data_access.query("SELECT id, username, name FROM User WHERE id = %s", user_id)
    except pymysql.MySQLError as e:
        raise RuntimeError(f'Database query error: {e}')

    # Convert to a dictionary for easier consumption
    return user


#  ADD User
def add_user(username, name):
    data_access = DataAccess()
    try:
        data_access.callproc("AddUser", (username, name,))
        last_row_id = data_access.get_lastrowid_for_callproc()
        # lastrowid = data_access.execute("INSERT INTO Users (username, name) VALUES (%s, %s);",
        #                                 (username, name))
        user = get_user(last_row_id)
        return user
    except Exception as e:
        raise e


