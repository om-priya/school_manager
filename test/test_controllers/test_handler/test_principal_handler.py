from src.controllers.handlers.principal_handler import PrincipalHandler
import pytest
import sqlite3


@pytest.fixture
def dummy_principal_handler_obj():
    dummy_obj = PrincipalHandler()
    return dummy_obj


@pytest.fixture
def set_mockeypatch_for_returning_query_valid_data(
    monkeypatch, mock_execute_returning_query_valid_data
):
    monkeypatch.setattr(
        "src.controllers.handlers.principal_handler.DatabaseAccess.execute_returning_query",
        mock_execute_returning_query_valid_data,
    )


@pytest.fixture
def set_mockeypatch_for_returning_query_with_no_data(
    monkeypatch, mock_execute_returning_query_no_data
):
    monkeypatch.setattr(
        "src.controllers.handlers.principal_handler.DatabaseAccess.execute_returning_query",
        mock_execute_returning_query_no_data,
    )


@pytest.fixture
def set_mockeypatch_for_returning_query_with_error(
    monkeypatch, mock_execute_returning_query_with_error
):
    monkeypatch.setattr(
        "src.controllers.handlers.principal_handler.DatabaseAccess.execute_returning_query",
        mock_execute_returning_query_with_error,
    )


@pytest.fixture
def set_mockeypatch_for_non_returning_query_with_error(
    monkeypatch, mock_execute_non_returning_query_with_error
):
    monkeypatch.setattr(
        "src.controllers.handlers.principal_handler.DatabaseAccess.execute_non_returning_query",
        mock_execute_non_returning_query_with_error,
    )


@pytest.fixture
def set_mockeypatch_for_non_returning_query_with_error(
    monkeypatch, mock_execute_non_returning_query
):
    monkeypatch.setattr(
        "src.controllers.handlers.principal_handler.DatabaseAccess.execute_non_returning_query",
        mock_execute_non_returning_query,
    )


def test_get_all_active_pid_without_error(
    set_mockeypatch_for_returning_query_valid_data,
):
    actual_data = PrincipalHandler.get_all_active_pid()
    assert [("om", "Priya"), ("Shreyansh", "Agrawal")] == actual_data


def test_get_all_active_pid_with_error(set_mockeypatch_for_returning_query_with_error):
    with pytest.raises(sqlite3.Error):
        actual_data = PrincipalHandler.get_all_active_pid()


def test_get_all_pending_id_with_error(set_mockeypatch_for_returning_query_with_error):
    with pytest.raises(sqlite3.Error):
        actual_data = PrincipalHandler.get_all_pending_id()


def test_get_all_pending_id_without_error(
    set_mockeypatch_for_returning_query_valid_data,
):
    actual_data = PrincipalHandler.get_all_pending_id()
    assert [("om", "Priya"), ("Shreyansh", "Agrawal")] == actual_data

