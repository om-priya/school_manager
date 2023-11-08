""" This Module contains database access class which will help in executing query """

import logging
from src.database.db_connector import DatabaseConnection
from src.config.sqlite_queries import DatabaseConfig

logger = logging.getLogger("db_logger")


# execute query of non returning type such as update, delete, insert
def execute_non_returning_query(query, params=None):
    """This function will execute the query of non returning type"""
    with DatabaseConnection(DatabaseConfig.DB_PATH) as connection:
        cursor = connection.cursor()
        if params is None:
            cursor.execute(query)
        else:
            cursor.execute(query, params)


# execute query of returning type such as read
def execute_returning_query(query, params=None):
    """This function will execute the query of returning type"""
    with DatabaseConnection(DatabaseConfig.DB_PATH) as connection:
        cursor = connection.cursor()
        if params is None:
            cursor.execute(query)
        else:
            cursor.execute(query, params)
        data_from_db = cursor.fetchall()
    return data_from_db
