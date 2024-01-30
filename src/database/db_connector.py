""" This Module is for creating context manager for db connection"""
import logging
import os
import mysql.connector
from config.sqlite_queries import DatabaseConfig

logger = logging.getLogger("db_logger")


class DatabaseConnection:
    """This class creates a context manager for database connection"""

    def __init__(self):
        self.connection = None

    def __enter__(self):
        self.connection = mysql.connector.connect(
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            host=os.getenv("HOST"),
        )
        cursor = self.connection.cursor()
        cursor.execute(DatabaseConfig.CREATE_DB)
        cursor.execute(DatabaseConfig.USE_DB)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_traceback):
        if exc_type or exc_val or exc_traceback:
            logger.error("Some error occurred")
            self.connection.close()
        else:
            self.connection.commit()
            self.connection.close()
