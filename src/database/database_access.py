""" This Module contains database access class which will help in executing query """

import logging
from src.database.db_connector import DatabaseConnection

logger = logging.getLogger("db_logger")


class DatabaseAccess:
    """This class will execute the query for operations"""

    _instance = None

    # to create singleton class
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseAccess, cls).__new__(cls)
        return cls._instance

    # execute query of non returning type such as update, delete, insert
    def execute_non_returning_query(self, query, params=None):
        """This function will execute the query of non returning type"""
        with DatabaseConnection("src\\database\\school.db") as connection:
            cursor = connection.cursor()
            if params is None:
                cursor.execute(query)
            else:
                cursor.execute(query, params)

    # execute query of returning type such as read
    def execute_returning_query(self, query, params=None):
        """This function will execute the query of returning type"""
        with DatabaseConnection("src\\database\\school.db") as connection:
            cursor = connection.cursor()
            if params is None:
                cursor.execute(query)
            else:
                cursor.execute(query, params)
            data_from_db = cursor.fetchall()
        return data_from_db
