from src.utils.initializer import initialize_app
import pytest
from src.database.db_connector import DatabaseConnection


@pytest.fixture
def mock_database_connection_for_initializer(mocker):
    mock_connection = mocker.MagicMock(spec=DatabaseConnection)
    mocker.patch(
        "src.utils.initializer.DatabaseConnection", return_value=mock_connection
    )
    mock_cursor = mocker.MagicMock()
    mock_connection.__enter__.return_value.cursor.return_value = mock_cursor
    mock_connection.__exit__.return_value = None
    return mock_cursor


def test_initialize_app(
    monkeypatch,
    mock_database_connection_for_initializer,
    mock_execute_returning_query_valid_data,
):
    mock_cursor = mock_database_connection_for_initializer
    monkeypatch.setattr(
        "src.utils.initializer.DatabaseAccess.execute_returning_query",
        mock_execute_returning_query_valid_data,
    )
    initialize_app()
    assert mock_cursor.execute.call_count == 12


def test_initialize_app(
    monkeypatch,
    mock_database_connection_for_initializer,
    mock_execute_returning_query_no_data,
):
    mock_cursor = mock_database_connection_for_initializer
    monkeypatch.setattr(
        "src.utils.initializer.DatabaseAccess.execute_returning_query",
        mock_execute_returning_query_no_data,
    )
    monkeypatch.setattr("src.utils.initializer.create_super_admin", lambda *args: None)
    initialize_app()
    assert mock_cursor.execute.call_count == 12
