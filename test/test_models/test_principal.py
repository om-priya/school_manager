from src.models.principals import Principal
import pytest
from src.database.db_connector import DatabaseConnection


@pytest.fixture
def dummy_principal_obj():
    principal_info = {
        "name": "Om Priya",
        "gender": "M",
        "email": "ompriya18153789@gmail.com",
        "phone": "8229070126",
        "school_name": "dav public school",
        "experience": "2",
        "password": "Ompriya@123",
    }
    dummy_obj = Principal(principal_info)
    return dummy_obj


@pytest.fixture
def mock_database_connection_for_principal(mocker):
    mock_connection = mocker.MagicMock(spec=DatabaseConnection)
    mocker.patch(
        "src.models.principals.DatabaseConnection", return_value=mock_connection
    )
    mock_cursor = mocker.MagicMock()
    mock_connection.__enter__.return_value.cursor.return_value = mock_cursor
    mock_connection.__exit__.return_value = None
    return mock_cursor


def test_save_principal_invalid_school_name(
    monkeypatch, mock_execute_returning_query_no_data, dummy_principal_obj, capsys
):
    monkeypatch.setattr(
        "src.models.teachers.DatabaseAccess.execute_returning_query",
        mock_execute_returning_query_no_data,
    )
    dummy_principal_obj.save_principal()
    captured = capsys.readouterr()

    assert "\nWrong School Or School is not in the system" in captured.out


def test_save_principal_valid_school_name(
    monkeypatch,
    mock_execute_returning_query_valid_data,
    dummy_principal_obj,
    mock_database_connection_for_principal,
    capsys,
):
    monkeypatch.setattr(
        "src.models.principals.DatabaseAccess.execute_returning_query",
        mock_execute_returning_query_valid_data,
    )
    monkeypatch.setattr(
        "src.models.principals.DatabaseConnection",
        mock_database_connection_for_principal,
    )
    dummy_principal_obj.save_principal()

    captured = capsys.readouterr()
    assert (
        "\nSigned Up Successfully Wait for Super Admin to approve it." in captured.out
    )
