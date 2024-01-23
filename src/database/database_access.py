""" This Module contains database access class which will help in executing query """
import logging
from database.db_connector import DatabaseConnection
from config.sqlite_queries import DatabaseConfig

logger = logging.getLogger("db_logger")


class DatabaseAccess:

    # execute query of non returning type such as update, delete, insert
    @classmethod
    def execute_non_returning_query(cls, query, params=None):
        """Execute a non-returning query (update, delete, insert)."""
        with DatabaseConnection() as connection:
            cursor = connection.cursor()
            if params is None:
                cursor.execute(query)
            else:
                cursor.execute(query, params)

    # execute query of returning type such as read
    @classmethod
    def execute_returning_query(cls, query, params=None):
        """Execute a returning query (read)."""
        with DatabaseConnection() as connection:
            cursor = connection.cursor(dictionary=True)
            if params is None:
                cursor.execute(query)
            else:
                cursor.execute(query, params)
            data_from_db = cursor.fetchall()
        return data_from_db
