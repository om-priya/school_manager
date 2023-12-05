import pytest
from src.controllers.principal_controller import PrincipalController
import builtins


@pytest.fixture
def mock_principal_controller_obj(mocker):
    mock_teacher_handler_ocj = mocker.Mock()
    mock_feedback_handler_ocj = mocker.Mock()
    mock_event_handler_ocj = mocker.Mock()
    mock_leave_handler_ocj = mocker.Mock()
    mock_issue_handler_ocj = mocker.Mock()
    mocker.patch(
        "src.controllers.principal_controller.TeacherHandler", mock_teacher_handler_ocj
    )
    mocker.patch(
        "src.controllers.principal_controller.FeedbackHandler",
        mock_feedback_handler_ocj,
    )
    mocker.patch(
        "src.controllers.principal_controller.EventHandler", mock_event_handler_ocj
    )
    mocker.patch(
        "src.controllers.principal_controller.LeaveHandler", mock_leave_handler_ocj
    )
    mocker.patch(
        "src.controllers.principal_controller.IssueHandler", mock_issue_handler_ocj
    )
    dummy_obj = PrincipalController("abcdef")
    return dummy_obj


class TestPrincipalController:
    def test_handle_teacher(self, monkeypatch, mock_principal_controller_obj, capsys):
        options = ["1", "2", "3", "4", "5", "ab", "6"]
        monkeypatch.setattr(builtins, "input", lambda *args: options.pop(0))
        mock_principal_controller_obj.handle_teacher()
        assert (
            mock_principal_controller_obj.teacher_handler_obj.approve_teacher.call_count
            == 1
        )
        assert (
            mock_principal_controller_obj.teacher_handler_obj.get_all_teacher.call_count
            == 1
        )
        assert (
            mock_principal_controller_obj.teacher_handler_obj.get_teacher_by_id.call_count
            == 1
        )
        assert (
            mock_principal_controller_obj.teacher_handler_obj.update_teacher.call_count
            == 1
        )
        assert (
            mock_principal_controller_obj.teacher_handler_obj.delete_teacher.call_count
            == 1
        )
        captured = capsys.readouterr()
        assert "\nInvalid Input Enter Only [1-6]\n" in captured.out

    def test_handle_feedbacks(self, monkeypatch, mock_principal_controller_obj, capsys):
        options = ["1", "2", "ab", "3"]
        monkeypatch.setattr(builtins, "input", lambda *args: options.pop(0))
        mock_principal_controller_obj.handle_feedbacks()
        assert (
            mock_principal_controller_obj.feedback_handler_obj.read_feedback.call_count
            == 1
        )
        assert (
            mock_principal_controller_obj.feedback_handler_obj.give_feedback.call_count
            == 1
        )
        captured = capsys.readouterr()
        assert "\nInvalid Input Enter Only [1-3]\n" in captured.out

    def test_handle_events(self, monkeypatch, mock_principal_controller_obj, capsys):
        options = ["1", "2", "ab", "3"]
        monkeypatch.setattr(builtins, "input", lambda *args: options.pop(0))
        mock_principal_controller_obj.handle_events()
        assert (
            mock_principal_controller_obj.event_handler_obj.read_event.call_count == 1
        )
        assert (
            mock_principal_controller_obj.event_handler_obj.create_event.call_count == 1
        )
        captured = capsys.readouterr()
        assert "\nInvalid Input Enter Only [1-3]\n" in captured.out

    def test_handle_leaves(self, monkeypatch, mock_principal_controller_obj, capsys):
        options = ["1", "2", "ab", "3"]
        monkeypatch.setattr(builtins, "input", lambda *args: options.pop(0))
        mock_principal_controller_obj.handle_leaves()
        assert (
            mock_principal_controller_obj.leave_handler_obj.see_leave_status.call_count
            == 1
        )
        assert (
            mock_principal_controller_obj.leave_handler_obj.apply_leave.call_count == 1
        )
        captured = capsys.readouterr()
        assert "\nInvalid Input Enter Only [1-3]\n" in captured.out

    def test_view_issue(self, mock_principal_controller_obj):
        mock_principal_controller_obj.view_issues()
        assert (
            mock_principal_controller_obj.issue_handler_obj.view_issue.call_count == 1
        )
