from src.database.db_connector import DatabaseConnection
import sqlite3
import pytest


class TestDatabaseConnection:
    def test_database_connection_class(self):
        with DatabaseConnection(":memory:") as conn:
            assert conn is not None

    def test_database_connection_class_error(self, caplog):
        with pytest.raises(sqlite3.Error):
            with DatabaseConnection(":memory:") as conn:
                raise sqlite3.Error
