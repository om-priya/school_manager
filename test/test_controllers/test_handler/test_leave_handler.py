from src.controllers.handlers.leave_handler import LeaveHandler
import pytest
import sqlite3


@pytest.fixture
def dummy_leave_handler_obj():
    dummy_obj = LeaveHandler("abc")
    return dummy_obj


# testing see_leave_status
def test_see_leave_status_with_no_data(
    monkeypatch, mock_execute_returning_query_no_data, dummy_leave_handler_obj, capsys
):
    monkeypatch.setattr(
        "src.controllers.handlers.leave_handler.DatabaseAccess.execute_returning_query",
        mock_execute_returning_query_no_data,
    )
    dummy_leave_handler_obj.see_leave_status()
    captured = capsys.readouterr()

    assert "" in captured.out


def test_see_leave_status_with_data(
    monkeypatch,
    mock_execute_returning_query_valid_data,
    dummy_leave_handler_obj,
    capsys,
):
    monkeypatch.setattr(
        "src.controllers.handlers.leave_handler.DatabaseAccess.execute_returning_query",
        mock_execute_returning_query_valid_data,
    )
    dummy_leave_handler_obj.see_leave_status()
    captured = capsys.readouterr()

    assert "om" in captured.out


def test_see_leave_status_with_error(
    monkeypatch,
    mock_execute_returning_query_with_error,
    dummy_leave_handler_obj,
    capsys,
):
    monkeypatch.setattr(
        "src.controllers.handlers.leave_handler.DatabaseAccess.execute_returning_query",
        mock_execute_returning_query_with_error,
    )
    dummy_leave_handler_obj.see_leave_status()
    captured = capsys.readouterr()

    assert "Something went wrong with db: \n" in captured.out


# apply leave status -- with error without error
def test_apply_leave_with_error(
    monkeypatch,
    mock_execute_non_returning_query_with_error,
    dummy_leave_handler_obj,
    capsys,
):
    monkeypatch.setattr(
        "src.controllers.handlers.leave_handler.DatabaseAccess.execute_non_returning_query",
        mock_execute_non_returning_query_with_error,
    )
    monkeypatch.setattr(
        "src.controllers.handlers.leave_handler.validate_date",
        lambda *args: "29-11-2050",
    )
    monkeypatch.setattr(
        "src.controllers.handlers.leave_handler.pattern_validator", lambda *args: 29
    )
    dummy_leave_handler_obj.apply_leave()

    captured = capsys.readouterr()
    assert "Something went wrong with db: \n" in captured.out


def test_apply_leave_without_error(
    monkeypatch,
    mock_execute_non_returning_query,
    dummy_leave_handler_obj,
    capsys,
):
    monkeypatch.setattr(
        "src.controllers.handlers.leave_handler.DatabaseAccess.execute_non_returning_query",
        mock_execute_non_returning_query,
    )
    monkeypatch.setattr(
        "src.controllers.handlers.leave_handler.validate_date",
        lambda *args: "29-11-2050",
    )
    monkeypatch.setattr(
        "src.controllers.handlers.leave_handler.pattern_validator", lambda *args: 29
    )
    dummy_leave_handler_obj.apply_leave()

    captured = capsys.readouterr()
    assert "\nLeave Request Added Successfully\n" in captured.out
