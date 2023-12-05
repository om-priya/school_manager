import pytest
from src.controllers.super_admin_controller import SuperAdminController
import builtins


@pytest.fixture
def mock_super_admin_controller_obj(mocker):
    mock_principal_handler_ocj = mocker.Mock()
    mock_staff_handler_ocj = mocker.Mock()
    mocker.patch(
        "src.controllers.super_admin_controller.PrincipalHandler",
        mock_principal_handler_ocj,
    )
    mocker.patch(
        "src.controllers.super_admin_controller.StaffHandler",
        mock_staff_handler_ocj,
    )
    dummy_obj = SuperAdminController("abcdef")
    return dummy_obj


class TestSuperAdminController:
    def test_handle_principal(
        self, monkeypatch, mock_super_admin_controller_obj, capsys
    ):
        options = ["1", "2", "3", "4", "5", "ab", "6"]
        monkeypatch.setattr(builtins, "input", lambda *args: options.pop(0))
        mock_super_admin_controller_obj.handle_principal()
        assert (
            mock_super_admin_controller_obj.principal_handler_obj.approve_principal.call_count
            == 1
        )
        assert (
            mock_super_admin_controller_obj.principal_handler_obj.get_all_principal.call_count
            == 1
        )
        assert (
            mock_super_admin_controller_obj.principal_handler_obj.get_principal_by_id.call_count
            == 1
        )
        assert (
            mock_super_admin_controller_obj.principal_handler_obj.update_principal.call_count
            == 1
        )
        assert (
            mock_super_admin_controller_obj.principal_handler_obj.delete_principal.call_count
            == 1
        )
        captured = capsys.readouterr()
        assert "\nInvalid Input Enter Only [1-6]\n" in captured.out

    def test_handle_staff(self, monkeypatch, mock_super_admin_controller_obj, capsys):
        options = ["1", "2", "3", "4", "ab", "5"]
        monkeypatch.setattr(builtins, "input", lambda *args: options.pop(0))
        mock_super_admin_controller_obj.handle_staff()
        assert (
            mock_super_admin_controller_obj.staff_handler_obj.view_staff.call_count == 1
        )
        assert (
            mock_super_admin_controller_obj.staff_handler_obj.create_staff.call_count
            == 1
        )
        assert (
            mock_super_admin_controller_obj.staff_handler_obj.update_staff.call_count
            == 1
        )
        assert (
            mock_super_admin_controller_obj.staff_handler_obj.delete_staff.call_count
            == 1
        )
        captured = capsys.readouterr()
        assert "\nInvalid Input Enter Only [1-5]\n" in captured.out

    def test_distribute_salary_with_both_teacher_and_principal(
        self,
        monkeypatch,
        mock_execute_returning_query_valid_data,
        mock_execute_non_returning_query,
        mock_super_admin_controller_obj,
        capsys,
    ):
        monkeypatch.setattr(
            "src.controllers.super_admin_controller.DatabaseAccess.execute_returning_query",
            mock_execute_returning_query_valid_data,
        )
        monkeypatch.setattr(
            "src.controllers.super_admin_controller.DatabaseAccess.execute_non_returning_query",
            mock_execute_non_returning_query,
        )
        mock_super_admin_controller_obj.distribute_salary()
        captured = capsys.readouterr()

        assert "Initiating Teacher Salary" in captured.out
        assert "Initiating Principal Salary" in captured.out

    def test_distribute_salary_with_no_teacher_no_principal(
        self,
        monkeypatch,
        mock_super_admin_controller_obj,
        mock_execute_returning_query_no_data,
        capsys,
    ):
        monkeypatch.setattr(
            "src.controllers.super_admin_controller.DatabaseAccess.execute_returning_query",
            mock_execute_returning_query_no_data,
        )
        mock_super_admin_controller_obj.distribute_salary()
        captured = capsys.readouterr()
        assert "\nNo such Teacher Found\n" in captured.out
        assert "\nNo such Principal Found\n" in captured.out

    def test_approve_leave_with_pending_request_valid_leave_id(
        self,
        monkeypatch,
        mock_execute_returning_query_valid_data,
        mock_execute_non_returning_query,
        mock_super_admin_controller_obj,
        capsys,
    ):
        monkeypatch.setattr(
            "src.controllers.super_admin_controller.DatabaseAccess.execute_returning_query",
            mock_execute_returning_query_valid_data,
        )
        monkeypatch.setattr(
            "src.controllers.super_admin_controller.validate.uuid_validator",
            lambda *args: "om",
        )
        monkeypatch.setattr(
            "src.controllers.super_admin_controller.DatabaseAccess.execute_non_returning_query",
            mock_execute_non_returning_query,
        )
        mock_super_admin_controller_obj.approve_leave()
        captured = capsys.readouterr()

        assert "\nLeave Added Successfully\n" in captured.out

    def test_approve_leave_with_no_pending_request(
        self,
        monkeypatch,
        mock_execute_returning_query_no_data,
        mock_super_admin_controller_obj,
        capsys,
    ):
        monkeypatch.setattr(
            "src.controllers.super_admin_controller.DatabaseAccess.execute_returning_query",
            mock_execute_returning_query_no_data,
        )
        mock_super_admin_controller_obj.approve_leave()
        captured = capsys.readouterr()

        assert "\nNo such Pending leave request Found\n" in captured.out

    def test_approve_leave_with_pending_request_invalid_id(
        self,
        monkeypatch,
        mock_execute_returning_query_valid_data,
        mock_super_admin_controller_obj,
        capsys,
    ):
        monkeypatch.setattr(
            "src.controllers.super_admin_controller.DatabaseAccess.execute_returning_query",
            mock_execute_returning_query_valid_data,
        )
        monkeypatch.setattr(
            "src.controllers.super_admin_controller.validate.uuid_validator",
            lambda *args: "millind",
        )
        mock_super_admin_controller_obj.approve_leave()
        captured = capsys.readouterr()

        assert "\nNo such Leave Record Found\n\n" in captured.out
