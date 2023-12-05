import pytest
from src.menu import UserScreen
import builtins


@pytest.fixture
def dummy_user_screen_obj():
    dummy_obj = UserScreen("AD23wq")
    return dummy_obj

class TestMenu:
    def test_super_admin_menu(self, monkeypatch, mocker, dummy_user_screen_obj, capsys):
        options = ["1", "2", "3", "4", "ab", "5", "6"]
        monkeypatch.setattr(builtins, "input", lambda *args: options.pop(0))
        mock_super_admin_controller_obj = mocker.Mock()
        mocker.patch(
            "src.menu.SuperAdminController", return_value=mock_super_admin_controller_obj
        )
        mock_change_password = mocker.Mock()
        mocker.patch(
            "src.menu.change_password",
            mock_change_password,
        )
        dummy_user_screen_obj.super_admin_menu()

        assert mock_super_admin_controller_obj.handle_principal.call_count == 1
        assert mock_super_admin_controller_obj.handle_staff.call_count == 1
        assert mock_super_admin_controller_obj.distribute_salary.call_count == 1
        assert mock_super_admin_controller_obj.approve_leave.call_count == 1
        mock_change_password.assert_called_once()

        captured = capsys.readouterr()

        assert "\nInvalid Input Enter only [1-6]\n" in captured.out


    def test_principal_menu(self, monkeypatch, mocker, dummy_user_screen_obj, capsys):
        options = ["1", "2", "3", "4", "ab", "5", "6", "7", "8", "9"]
        monkeypatch.setattr(builtins, "input", lambda *args: options.pop(0))
        mock_principal_controller_obj = mocker.Mock()
        mocker.patch(
            "src.menu.PrincipalController", return_value=mock_principal_controller_obj
        )
        mock_change_password = mocker.Mock()
        mocker.patch(
            "src.menu.change_password",
            mock_change_password,
        )
        dummy_user_screen_obj.principal_menu()

        assert mock_principal_controller_obj.handle_teacher.call_count == 1
        assert mock_principal_controller_obj.handle_feedbacks.call_count == 1
        assert mock_principal_controller_obj.handle_events.call_count == 1
        assert mock_principal_controller_obj.handle_leaves.call_count == 1
        assert mock_principal_controller_obj.view_profile.call_count == 1
        assert mock_principal_controller_obj.see_salary_history.call_count == 1
        assert mock_principal_controller_obj.view_issues.call_count == 1
        mock_change_password.assert_called_once()

        captured = capsys.readouterr()

        assert "\nInvalid Input Enter only [1-9]\n" in captured.out


    def test_teacher_menu(self, monkeypatch, mocker, dummy_user_screen_obj, capsys):
        options = ["1", "2", "3", "4", "ab", "5", "6", "7", "8"]
        monkeypatch.setattr(builtins, "input", lambda *args: options.pop(0))
        mock_teacher_controller_obj = mocker.Mock()
        mocker.patch(
            "src.menu.TeacherController", return_value=mock_teacher_controller_obj
        )
        mock_change_password = mocker.Mock()
        mocker.patch(
            "src.menu.change_password",
            mock_change_password,
        )
        dummy_user_screen_obj.teacher_menu()

        assert mock_teacher_controller_obj.view_profile.call_count == 1
        assert mock_teacher_controller_obj.read_notice.call_count == 1
        assert mock_teacher_controller_obj.read_feedbacks.call_count == 1
        assert mock_teacher_controller_obj.raise_issue.call_count == 1
        assert mock_teacher_controller_obj.salary_history.call_count == 1
        assert mock_teacher_controller_obj.handle_leaves.call_count == 1
        mock_change_password.assert_called_once()

        captured = capsys.readouterr()

        assert "\nInvalid Input Enter only [1-8]\n" in captured.out
