""" This Module is for creating context manager for db connection"""

import logging
import os
import mysql.connector
import pymysql
from config.sqlite_queries import DatabaseConfig
from helper.helper_function import get_request_id

logger = logging.getLogger("db_logger")


class DatabaseConnection:
    """This class creates a context manager for database connection"""

    def __init__(self):
        self.connection = None

    def __enter__(self):
        self.connection = pymysql.connect(
            port=int(os.getenv("DB_PORT")),
            cursorclass=pymysql.cursors.DictCursor,
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )
        cursor = self.connection.cursor()
        cursor.execute(DatabaseConfig.CREATE_DB)
        cursor.execute(DatabaseConfig.USE_DB)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_traceback):
        if exc_type or exc_val or exc_traceback:
            logger.info(
                f"Something went Wrong with Db {exc_type} {exc_val} {exc_traceback}"
            )
            self.connection.close()
        else:
            self.connection.commit()
            self.connection.close()
