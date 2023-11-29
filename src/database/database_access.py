""" This Module contains database access class which will help in executing query """
import logging
from database.db_connector import DatabaseConnection
from config.sqlite_queries import DatabaseConfig

logger = logging.getLogger("db_logger")


class DatabaseAccess:
    DB_PATH = DatabaseConfig.DB_PATH

    # execute query of non returning type such as update, delete, insert
    @classmethod
    def execute_non_returning_query(cls, query, params=None):
        """This function will execute the query of non returning type"""
        with DatabaseConnection(cls.DB_PATH) as connection:
            cursor = connection.cursor()
            if params is None:
                cursor.execute(query)
            else:
                cursor.execute(query, params)

    # execute query of returning type such as read
    @classmethod
    def execute_returning_query(cls, query, params=None):
        """This function will execute the query of returning type"""
        with DatabaseConnection(cls.DB_PATH) as connection:
            cursor = connection.cursor()
            if params is None:
                cursor.execute(query)
            else:
                cursor.execute(query, params)
            data_from_db = cursor.fetchall()
        return data_from_db
