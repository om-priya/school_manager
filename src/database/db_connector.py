""" This Module is for creating context manager for db connection"""
import logging
import os
import mysql.connector
import sqlite3

logger = logging.getLogger("db_logger")


class DatabaseConnection:
    """This class creates a context manager for database connection"""

    def __init__(self, host):
        self.connection = None
        self.host = host

    def __enter__(self):
        self.connection = mysql.connector.connect(
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            host=os.getenv("HOST"),
        )
        # self.connection = sqlite3.connect(self.host)
        cursor = self.connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS mydb")
        cursor.execute("USE mydb")
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_traceback):
        if exc_type or exc_val or exc_traceback:
            logger.error("Some error occurred")
            self.connection.close()
        else:
            self.connection.commit()
            self.connection.close()
