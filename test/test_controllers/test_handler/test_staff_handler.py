from src.controllers.handlers.staff_handler import StaffHandler
import pytest
import builtins


@pytest.fixture
def dummy_staff_handler_obj():
    dummy_obj = StaffHandler("abc")
    return dummy_obj


class TestStaffHandler:
    def test_fetch_staff_status(
        self, monkeypatch, mock_execute_returning_query_valid_data
    ):
        monkeypatch.setattr(
            "src.controllers.handlers.staff_handler.DatabaseAccess.execute_returning_query",
            mock_execute_returning_query_valid_data,
        )
        data = StaffHandler.fetch_staff_status("")
        assert "om" == data[0][0]

    def test_check_staff_no_staff(self, monkeypatch, dummy_staff_handler_obj):
        monkeypatch.setattr(
            "src.controllers.handlers.staff_handler.StaffHandler.fetch_staff_status",
            lambda *args: [],
        )
        actual_result = dummy_staff_handler_obj.check_staff("def")

        assert actual_result == False

    def test_check_staff_active_staff(self, monkeypatch, dummy_staff_handler_obj):
        monkeypatch.setattr(
            "src.controllers.handlers.staff_handler.StaffHandler.fetch_staff_status",
            lambda *args: [("active",)],
        )
        actual_result = dummy_staff_handler_obj.check_staff("def")

        assert actual_result

    def test_view_staff_no_data(
        self,
        monkeypatch,
        mock_execute_returning_query_no_data,
        dummy_staff_handler_obj,
        capsys,
    ):
        monkeypatch.setattr(
            "src.controllers.handlers.staff_handler.DatabaseAccess.execute_returning_query",
            mock_execute_returning_query_no_data,
        )
        dummy_staff_handler_obj.view_staff()

        captured = capsys.readouterr()
        assert "\nNo such Staff Found\n" in captured.out

    def test_view_staff_with_data(
        self,
        monkeypatch,
        mock_execute_returning_query_valid_data,
        dummy_staff_handler_obj,
        capsys,
    ):
        monkeypatch.setattr(
            "src.controllers.handlers.staff_handler.DatabaseAccess.execute_returning_query",
            mock_execute_returning_query_valid_data,
        )
        dummy_staff_handler_obj.view_staff()

        captured = capsys.readouterr()
        assert "om" in captured.out

    def test_create_staff(
        self,
        monkeypatch,
        mock_execute_returning_query_valid_data,
        mock_execute_non_returning_query,
        dummy_staff_handler_obj,
        capsys,
    ):
        staff_data = ["Om", "Python", "8787878787", "Noida", "m"]
        monkeypatch.setattr(
            "src.controllers.handlers.staff_handler.validate.pattern_validator",
            lambda *args: staff_data.pop(0),
        )
        monkeypatch.setattr(
            "src.controllers.handlers.staff_handler.DatabaseAccess.execute_returning_query",
            mock_execute_returning_query_valid_data,
        )
        monkeypatch.setattr(
            "src.controllers.handlers.staff_handler.DatabaseAccess.execute_non_returning_query",
            mock_execute_non_returning_query,
        )
        dummy_staff_handler_obj.create_staff()

        captured = capsys.readouterr()
        assert "\nStaff Added Successfully\n" in captured.out

    @pytest.mark.parametrize("field_to_update", ["name", "phone", "gender"])
    def test_update_staff(
        self,
        monkeypatch,
        dummy_staff_handler_obj,
        mock_execute_non_returning_query,
        field_to_update,
        capsys,
    ):
        monkeypatch.setattr(
            "src.controllers.handlers.staff_handler.validate.uuid_validator",
            lambda *args: "abc1AS",
        )
        monkeypatch.setattr(
            "src.controllers.handlers.staff_handler.StaffHandler.check_staff",
            lambda *args: True,
        )
        monkeypatch.setattr(builtins, "input", lambda *args: field_to_update)
        monkeypatch.setattr(
            "src.controllers.handlers.staff_handler.validate.pattern_validator",
            lambda *args: "dummy value",
        )
        monkeypatch.setattr(
            "src.controllers.handlers.staff_handler.DatabaseAccess.execute_non_returning_query",
            mock_execute_non_returning_query,
        )
        dummy_staff_handler_obj.update_staff()
        captured = capsys.readouterr()

        assert "\nUpdated Successfully" in captured.out

    def test_update_staff_invalid_staff(
        self,
        monkeypatch,
        dummy_staff_handler_obj,
        capsys,
    ):
        monkeypatch.setattr(
            "src.controllers.handlers.staff_handler.validate.uuid_validator",
            lambda *args: "abc1AS",
        )
        monkeypatch.setattr(
            "src.controllers.handlers.staff_handler.StaffHandler.check_staff",
            lambda *args: False,
        )
        dummy_staff_handler_obj.update_staff()
        captured = capsys.readouterr()

        assert "\nNo such Staff Found\n" in captured.out

    def test_delete_staff_with_invalid_staff(
        self, monkeypatch, dummy_staff_handler_obj, capsys
    ):
        monkeypatch.setattr(
            "src.controllers.handlers.staff_handler.validate.uuid_validator",
            lambda *args: "abc1AS",
        )
        monkeypatch.setattr(
            "src.controllers.handlers.staff_handler.StaffHandler.check_staff",
            lambda *args: False,
        )
        dummy_staff_handler_obj.delete_staff()
        captured = capsys.readouterr()

        assert "\nNo such Staff Found\n" in captured.out

    def test_delete_staff_with_valid_staff(
        self,
        monkeypatch,
        dummy_staff_handler_obj,
        mock_execute_non_returning_query,
        capsys,
    ):
        monkeypatch.setattr(
            "src.controllers.handlers.staff_handler.validate.uuid_validator",
            lambda *args: "abc1AS",
        )
        monkeypatch.setattr(
            "src.controllers.handlers.staff_handler.StaffHandler.check_staff",
            lambda *args: True,
        )
        monkeypatch.setattr(
            "src.controllers.handlers.staff_handler.DatabaseAccess.execute_non_returning_query",
            mock_execute_non_returning_query,
        )
        dummy_staff_handler_obj.delete_staff()
        captured = capsys.readouterr()

        assert "\nDeleted Successfully" in captured.out
