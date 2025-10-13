import pymysql

from database.data_access import DataAccess

#  GET ALL Users
def get_users(username=None, name=None):
    data_access = DataAccess()
    try:
        if username:
            users = data_access.query("SELECT id, username, name FROM Users WHERE username = %s", username)
        elif name:
            users = data_access.query("SELECT id, username, name FROM Users WHERE name = %s", name)
        else:
            users = data_access.query("SELECT id, username, name FROM Users")
    except pymysql.MySQLError as e:
        raise RuntimeError(f'Database query error: {e}')

    # Convert to a dictionary for easier consumption
    return users


#  GET a specific user
def get_user(user_id):
    data_access = DataAccess()
    try:
        user = data_access.query("SELECT id, username, name FROM Users WHERE id = %s", user_id)
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


