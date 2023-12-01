import pytest
from src.controllers.teacher_controller import TeacherController
import builtins


@pytest.fixture
def mock_super_admin_controller_obj(mocker):
    mock_event_handler_obj = mocker.Mock()
    mock_leave_handler_obj = mocker.Mock()
    mock_issue_handler_obj = mocker.Mock()
    mocker.patch(
        "src.controllers.teacher_controller.EventHandler",
        mock_event_handler_obj,
    )
    mocker.patch(
        "src.controllers.teacher_controller.LeaveHandler",
        mock_leave_handler_obj,
    )
    mocker.patch(
        "src.controllers.teacher_controller.IssueHandler",
        mock_issue_handler_obj,
    )
    dummy_obj = TeacherController("abcdef")
    return dummy_obj


def test_read_notice(mock_super_admin_controller_obj):
    mock_super_admin_controller_obj.read_notice()
    assert mock_super_admin_controller_obj.event_handler_obj.read_event.call_count == 1


def test_raise_issue(mock_super_admin_controller_obj):
    mock_super_admin_controller_obj.raise_issue()
    assert mock_super_admin_controller_obj.issue_handler_obj.raise_issue.call_count == 1


def test_handle_leaves(monkeypatch, mock_super_admin_controller_obj, capsys):
    options = ["1", "2", "ab", "3"]
    monkeypatch.setattr(builtins, "input", lambda *args: options.pop(0))
    mock_super_admin_controller_obj.handle_leaves()
    assert (
        mock_super_admin_controller_obj.leave_handler_obj.see_leave_status.call_count
        == 1
    )
    assert mock_super_admin_controller_obj.leave_handler_obj.apply_leave.call_count == 1

    captured = capsys.readouterr()
    assert "\nInvalid Input Enter Only [1-3]\n" in captured.out


def test_read_feedbacks_no_data(
    monkeypatch,
    mock_execute_returning_query_no_data,
    mock_super_admin_controller_obj,
    capsys,
):
    monkeypatch.setattr(
        "src.controllers.teacher_controller.DatabaseAccess.execute_returning_query",
        mock_execute_returning_query_no_data,
    )
    mock_super_admin_controller_obj.read_feedbacks()
    captured = capsys.readouterr()
    assert "\nNo such Feedback Found\n" in captured.out


def test_read_feedbacks_with_data(
    monkeypatch,
    mock_execute_returning_query_valid_data,
    mock_super_admin_controller_obj,
    capsys,
):
    monkeypatch.setattr(
        "src.controllers.teacher_controller.DatabaseAccess.execute_returning_query",
        mock_execute_returning_query_valid_data,
    )
    mock_super_admin_controller_obj.read_feedbacks()
    captured = capsys.readouterr()
    assert "om" in captured.out
