from src.controllers.handlers.teacher_handler import TeacherHandler
import pytest


@pytest.fixture
def dummy_teacher_handler_obj():
    dummy_obj = TeacherHandler()
    return dummy_obj


def test_get_status(monkeypatch, mock_execute_returning_query_no_data):
    monkeypatch.setattr(
        "src.controllers.handlers.teacher_handler.DatabaseAccess.execute_returning_query",
        mock_execute_returning_query_no_data,
    )
    expected_result = TeacherHandler.get_status("abc")

    assert len(expected_result) == 0


def test_fetch_active_teacher(monkeypatch):
    monkeypatch.setattr(
        "src.controllers.handlers.teacher_handler.DatabaseAccess.execute_returning_query",
        lambda *args: [("active",)],
    )
    expected_result = TeacherHandler.get_status("abc")

    assert expected_result[0][0] == "active"


def test_approve_teacher_no_teacher(monkeypatch, dummy_teacher_handler_obj, capsys):
    monkeypatch.setattr(
        "src.controllers.handlers.teacher_handler.validate.uuid_validator",
        lambda *args: "abcd",
    )
    monkeypatch.setattr(
        "src.controllers.handlers.teacher_handler.TeacherHandler.get_status",
        lambda *args: [],
    )
    dummy_teacher_handler_obj.approve_teacher()
    captured = capsys.readouterr()

    assert "\nNo such Teachers Found\n" in captured.out


def test_approve_teacher_not_pending_teacher(
    monkeypatch, dummy_teacher_handler_obj, capsys
):
    monkeypatch.setattr(
        "src.controllers.handlers.teacher_handler.validate.uuid_validator",
        lambda *args: "abcd",
    )
    monkeypatch.setattr(
        "src.controllers.handlers.teacher_handler.TeacherHandler.get_status",
        lambda *args: [("active",)],
    )
    dummy_teacher_handler_obj.approve_teacher()
    captured = capsys.readouterr()

    assert "\nTeacher Can't be Approved" in captured.out


def test_approve_teacher_pending_teacher(
    monkeypatch, dummy_teacher_handler_obj, mock_execute_non_returning_query, capsys
):
    monkeypatch.setattr(
        "src.controllers.handlers.teacher_handler.validate.uuid_validator",
        lambda *args: "abcd",
    )
    monkeypatch.setattr(
        "src.controllers.handlers.teacher_handler.TeacherHandler.get_status",
        lambda *args: [("pending",)],
    )
    monkeypatch.setattr(
        "src.controllers.handlers.teacher_handler.DatabaseAccess.execute_non_returning_query",
        mock_execute_non_returning_query,
    )
    dummy_teacher_handler_obj.approve_teacher()
    captured = capsys.readouterr()

    assert "\nTeacher Added Successfully\n" in captured.out


def test_get_all_teacher_no_data(
    monkeypatch, dummy_teacher_handler_obj, mock_execute_returning_query_no_data, capsys
):
    monkeypatch.setattr(
        "src.controllers.handlers.teacher_handler.DatabaseAccess.execute_returning_query",
        mock_execute_returning_query_no_data,
    )
    dummy_teacher_handler_obj.get_all_teacher()
    captured = capsys.readouterr()

    assert "\nNo such Teachers Found\n" in captured.out


def test_get_all_teacher_with_data(
    monkeypatch,
    dummy_teacher_handler_obj,
    mock_execute_returning_query_valid_data,
    capsys,
):
    monkeypatch.setattr(
        "src.controllers.handlers.teacher_handler.DatabaseAccess.execute_returning_query",
        mock_execute_returning_query_valid_data,
    )
    dummy_teacher_handler_obj.get_all_teacher()
    captured = capsys.readouterr()

    assert "om" in captured.out


def test_get_teacher_by_id_valid_id(
    monkeypatch,
    dummy_teacher_handler_obj,
    mock_execute_returning_query_valid_data,
    capsys,
):
    monkeypatch.setattr(
        "src.controllers.handlers.teacher_handler.validate.uuid_validator",
        lambda *args: "ACse35",
    )
    monkeypatch.setattr(
        "src.controllers.handlers.teacher_handler.DatabaseAccess.execute_returning_query",
        mock_execute_returning_query_valid_data,
    )
    dummy_teacher_handler_obj.get_teacher_by_id()
    captured = capsys.readouterr()

    assert "om" in captured.out


def test_get_teacher_by_id_invalid_id(
    monkeypatch,
    dummy_teacher_handler_obj,
    mock_execute_returning_query_no_data,
    capsys,
):
    monkeypatch.setattr(
        "src.controllers.handlers.teacher_handler.validate.uuid_validator",
        lambda *args: "ACse35",
    )
    monkeypatch.setattr(
        "src.controllers.handlers.teacher_handler.DatabaseAccess.execute_returning_query",
        mock_execute_returning_query_no_data,
    )
    dummy_teacher_handler_obj.get_teacher_by_id()
    captured = capsys.readouterr()

    assert "\nNo such Teachers Found\n" in captured.out


def test_delete_teacher_no_active_teacher(
    monkeypatch, mock_execute_returning_query_no_data, dummy_teacher_handler_obj, capsys
):
    monkeypatch.setattr(
        "src.controllers.handlers.teacher_handler.validate.uuid_validator",
        lambda *args: "om",
    )
    monkeypatch.setattr(
        "src.controllers.handlers.teacher_handler.TeacherHandler.fetch_active_teacher",
        mock_execute_returning_query_no_data,
    )
    dummy_teacher_handler_obj.delete_teacher()

    captured = capsys.readouterr()

    assert "\nNo such Teachers Found\n" in captured.out


def test_delete_teacher_incorrect_teacher_id(
    monkeypatch, mock_execute_returning_query_valid_data, dummy_teacher_handler_obj ,capsys
):
    monkeypatch.setattr(
        "src.controllers.handlers.teacher_handler.validate.uuid_validator",
        lambda *args: "millind",
    )
    monkeypatch.setattr(
        "src.controllers.handlers.teacher_handler.TeacherHandler.fetch_active_teacher",
        mock_execute_returning_query_valid_data,
    )
    dummy_teacher_handler_obj.delete_teacher()

    captured = capsys.readouterr()

    assert "\nCan't perform Delete action on entered user_id" in captured.out


def test_delete_teacher_correct_teacher_id(
    monkeypatch,
    mock_execute_returning_query_valid_data,
    dummy_teacher_handler_obj,
    mock_execute_non_returning_query,
    capsys,
):
    monkeypatch.setattr(
        "src.controllers.handlers.teacher_handler.validate.uuid_validator",
        lambda *args: "om",
    )
    monkeypatch.setattr(
        "src.controllers.handlers.teacher_handler.TeacherHandler.fetch_active_teacher",
        mock_execute_returning_query_valid_data,
    )
    monkeypatch.setattr(
        "src.controllers.handlers.teacher_handler.DatabaseAccess.execute_non_returning_query",
        mock_execute_non_returning_query,
    )
    dummy_teacher_handler_obj.delete_teacher()
    captured = capsys.readouterr()

    assert "\nDeleted Successfully" in captured.out
