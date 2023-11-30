from src.database.db_connector import DatabaseConnection


def test_database_connection_class():
    with DatabaseConnection(":memory:") as conn:
        assert conn is not None
