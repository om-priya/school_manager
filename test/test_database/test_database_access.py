from src.database.database_access import DatabaseAccess


class TestDatabaseAccess:
    def test_execute_non_returning_query_with_params(self, mock_database_connection):
        query = ""
        params = [("om",), ("Priya",)]
        mock_cursor = mock_database_connection
        DatabaseAccess.execute_non_returning_query(query, params=params)
        assert mock_cursor.execute.call_count == 1
        mock_cursor.execute.assert_called_with(query, params)

    def test_execute_non_returning_query_without_params(self, mock_database_connection):
        query = ""
        params = None
        mock_cursor = mock_database_connection
        DatabaseAccess.execute_non_returning_query(query, params=params)
        assert mock_cursor.execute.call_count == 1
        mock_cursor.execute.assert_called_with(query)

    def test_execute_returning_query_with_params(self, mock_database_connection):
        query = ""
        params = [("om",), ("Priya",)]
        mock_cursor = mock_database_connection
        DatabaseAccess.execute_returning_query(query, params=params)
        assert mock_cursor.execute.call_count == 1
        assert mock_cursor.fetchall.call_count == 1
        mock_cursor.execute.assert_called_with(query, params)

    def test_execute_returning_query_without_params(self, mock_database_connection):
        query = ""
        mock_cursor = mock_database_connection
        DatabaseAccess.execute_returning_query(query)
        assert mock_cursor.execute.call_count == 1
        assert mock_cursor.fetchall.call_count == 1
        mock_cursor.execute.assert_called_with(query)
