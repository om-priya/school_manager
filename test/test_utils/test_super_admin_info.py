from src.utils.super_admin_info import create_super_admin
import pytest
from src.database.db_connector import DatabaseConnection


@pytest.fixture
def mock_database_connection_for_super_admin_info(mocker):
    mock_connection = mocker.MagicMock(spec=DatabaseConnection)
    mocker.patch(
        "src.utils.super_admin_info.DatabaseConnection", return_value=mock_connection
    )
    mock_cursor = mocker.MagicMock()
    mock_connection.__enter__.return_value.cursor.return_value = mock_cursor
    mock_connection.__exit__.return_value = None
    return mock_cursor


def test_create_super_admin(monkeypatch, mock_database_connection_for_super_admin_info):
    monkeypatch.setenv("NAME", "TestingName")
    monkeypatch.setenv("GENDER", "m")
    monkeypatch.setenv("EMAIL", "abc@gmail.com")
    monkeypatch.setenv("PHONE", "1234567878")
    monkeypatch.setenv("ROLE", "Test Super Admin")
    monkeypatch.setenv("STATUS", "Active")
    monkeypatch.setenv("USER_NAME", "abc")
    monkeypatch.setenv("PASSWORD", "TestingPassword")
    monkeypatch.setenv("SCHOOL_NAME", "dav public school")
    monkeypatch.setenv("SCHOOL_LOCATION", "Noida")
    monkeypatch.setenv("SCHOOL_EMAIL", "school@gmail.com")
    monkeypatch.setenv("SCHOOL_CONTACT", "3232323232")

    mock_cursor = mock_database_connection_for_super_admin_info
    create_super_admin()

    assert mock_cursor.execute.call_count == 4
