import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

class DataAccess:
    def __init__(self):
        self.__connection = None
        self.__cursor = None
        self._connect()

    def _connect(self):
        if not self.__connection or not self.__connection.open:
            try:
                self.__connection = pymysql.connect(
                    host=os.getenv("DB_HOST"),
                    user=os.getenv("DB_USER"),
                    db=os.getenv("DB_NAME"),
                    password=os.getenv("DB_PASSWORD"),
                    cursorclass=pymysql.cursors.DictCursor,
                )
                self.__cursor = self.__connection.cursor()
            except pymysql.MySQLError as e:
                raise RuntimeError(f'Database connection error: {e}')

    def __del__(self):
        self.close()

    def close(self):
        if self.__cursor:
            try:
                self.__cursor.close()
            except pymysql.MySQLError:
                pass

        if self.__connection:
            try:
                self.__connection.close()
            except pymysql.MySQLError:
                pass

    def query(self, query, params=None):
        try:
            self._connect()
            self.__cursor.execute(query, params)
            return self.__cursor.fetchall()
        except pymysql.MySQLError as e:
            raise RuntimeError(f'Database query error: {e}')

    def execute(self, query, params=None):
        try:
            self._connect()
            self.__cursor.execute(query, params)
            self.__connection.commit()
            return self.__cursor.lastrowid
        except pymysql.MySQLError as e:
            self.__connection.rollback()
            raise RuntimeError(f"Database query execution failed: {e}")

    def callproc(self, stored_procedure, params=()):
        try:
            self._connect()
            self.__cursor.callproc(stored_procedure, params)
            self.__connection.commit()
            return self.__cursor.fetchall()
        except pymysql.MySQLError as e:
            self.__connection.rollback()
            raise RuntimeError(f"Database query execution failed: {e}")

    def getlastrowid_for_callproc(self):
        try:
            returned_result = self.__cursor.execute("SELECT LAST_INSERT_ID();")
            lastrowid = self.__cursor.fetchone()['LAST_INSERT_ID()']
            return lastrowid
        except pymysql.MySQLError as e:
            raise RuntimeError(f"Database query execution failed: {e}")