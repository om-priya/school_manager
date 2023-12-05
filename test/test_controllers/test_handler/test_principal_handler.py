from src.controllers.handlers.principal_handler import PrincipalHandler
import pytest
import sqlite3
import builtins


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
def set_mockeypatch_for_non_returning_query_without_error(
    monkeypatch, mock_execute_non_returning_query
):
    monkeypatch.setattr(
        "src.controllers.handlers.principal_handler.DatabaseAccess.execute_non_returning_query",
        mock_execute_non_returning_query,
    )


class TestPrincipalHandler:
    def test_get_all_active_pid_without_error(
        self,
        set_mockeypatch_for_returning_query_valid_data,
    ):
        actual_data = PrincipalHandler.get_all_active_pid()
        assert [("om", "Priya"), ("Shreyansh", "Agrawal")] == actual_data

    def test_get_all_active_pid_with_error(
        self,
        set_mockeypatch_for_returning_query_with_error,
    ):
        with pytest.raises(sqlite3.Error):
            actual_data = PrincipalHandler.get_all_active_pid()

    def test_get_all_pending_id_with_error(
        self,
        set_mockeypatch_for_returning_query_with_error,
    ):
        with pytest.raises(sqlite3.Error):
            actual_data = PrincipalHandler.get_all_pending_id()

    def test_get_all_pending_id_without_error(
        self,
        set_mockeypatch_for_returning_query_valid_data,
    ):
        actual_data = PrincipalHandler.get_all_pending_id()
        assert [("om", "Priya"), ("Shreyansh", "Agrawal")] == actual_data

    def test_approve_principal_with_active_principal(
        self, monkeypatch, dummy_principal_handler_obj, capsys
    ):
        monkeypatch.setattr(
            "src.controllers.handlers.principal_handler.validate.uuid_validator",
            lambda *args: "abc",
        )
        monkeypatch.setattr(
            dummy_principal_handler_obj, "get_all_active_pid", lambda *args: [("abc",)]
        )
        dummy_principal_handler_obj.approve_principal()
        captured = capsys.readouterr()
        assert "\nCan't add more than one principal" in captured.out

    def test_approve_principal_with_no_active_no_pending(
        self, monkeypatch, dummy_principal_handler_obj, capsys
    ):
        monkeypatch.setattr(
            "src.controllers.handlers.principal_handler.validate.uuid_validator",
            lambda *args: "abc",
        )
        monkeypatch.setattr(
            dummy_principal_handler_obj, "get_all_active_pid", lambda *args: []
        )
        monkeypatch.setattr(
            dummy_principal_handler_obj, "get_all_active_pid", lambda *args: []
        )
        dummy_principal_handler_obj.approve_principal()
        captured = capsys.readouterr()
        assert "\nNo such request for approval Found\n" in captured.out

    def test_approve_principal_with_no_active_invalid_id(
        self, monkeypatch, dummy_principal_handler_obj, capsys
    ):
        monkeypatch.setattr(
            "src.controllers.handlers.principal_handler.validate.uuid_validator",
            lambda *args: "abc",
        )
        monkeypatch.setattr(
            dummy_principal_handler_obj, "get_all_active_pid", lambda *args: []
        )
        monkeypatch.setattr(
            dummy_principal_handler_obj,
            "get_all_pending_id",
            lambda *args: [("om",), ("Shreyansh",)],
        )
        dummy_principal_handler_obj.approve_principal()
        captured = capsys.readouterr()
        assert "\nNo such Principal Found\n" in captured.out

    def test_approve_principal_with_no_active_valid_id(
        self,
        monkeypatch,
        dummy_principal_handler_obj,
        mock_execute_non_returning_query,
        capsys,
    ):
        monkeypatch.setattr(
            "src.controllers.handlers.principal_handler.validate.uuid_validator",
            lambda *args: "om",
        )
        monkeypatch.setattr(
            dummy_principal_handler_obj, "get_all_active_pid", lambda *args: []
        )
        monkeypatch.setattr(
            dummy_principal_handler_obj,
            "get_all_pending_id",
            lambda *args: [("om",), ("Shreyansh",)],
        )
        dummy_principal_handler_obj.approve_principal()
        captured = capsys.readouterr()
        assert "\nPrincipal Added Successfully\n" in captured.out

    def test_get_all_principal_with_no_data(
        self,
        set_mockeypatch_for_returning_query_with_no_data,
        dummy_principal_handler_obj,
        capsys,
    ):
        dummy_principal_handler_obj.get_all_principal()
        captured = capsys.readouterr()
        assert "\nNo such Principal Found\n" in captured.out

    def test_get_all_principal_with_data(
        self,
        set_mockeypatch_for_returning_query_valid_data,
        dummy_principal_handler_obj,
        capsys,
    ):
        dummy_principal_handler_obj.get_all_principal()
        captured = capsys.readouterr()
        assert "om" in captured.out

    def test_get_principal_by_id_with_no_data(
        self,
        monkeypatch,
        set_mockeypatch_for_returning_query_with_no_data,
        dummy_principal_handler_obj,
        capsys,
    ):
        monkeypatch.setattr(
            "src.controllers.handlers.principal_handler.validate.uuid_validator",
            lambda *args: "om",
        )
        dummy_principal_handler_obj.get_principal_by_id()
        captured = capsys.readouterr()
        assert "\nNo such Principal Found\n" in captured.out

    def test_get_principal_by_id_with_data(
        self,
        monkeypatch,
        set_mockeypatch_for_returning_query_valid_data,
        dummy_principal_handler_obj,
        capsys,
    ):
        monkeypatch.setattr(
            "src.controllers.handlers.principal_handler.validate.uuid_validator",
            lambda *args: "om",
        )
        dummy_principal_handler_obj.get_principal_by_id()
        captured = capsys.readouterr()
        assert "om" in captured.out

    @pytest.mark.parametrize(
        "field_to_update", ["name", "gender", "email", "phone", "experience"]
    )
    def test_update_principal(
        self,
        monkeypatch,
        field_to_update,
        mock_execute_non_returning_query,
        dummy_principal_handler_obj,
        capsys,
    ):
        monkeypatch.setattr(
            "src.controllers.handlers.principal_handler.validate.uuid_validator",
            lambda *args: "abc",
        )
        monkeypatch.setattr(builtins, "input", lambda *args: field_to_update)
        monkeypatch.setattr(
            dummy_principal_handler_obj, "get_all_active_pid", lambda *args: [("abc",)]
        )
        monkeypatch.setattr(
            "src.controllers.handlers.principal_handler.validate.pattern_validator",
            lambda *args: "dummy data",
        )
        monkeypatch.setattr(
            "src.controllers.handlers.principal_handler.DatabaseAccess.execute_non_returning_query",
            mock_execute_non_returning_query,
        )
        dummy_principal_handler_obj.update_principal()
        captured = capsys.readouterr()

        assert "\nUpdated Successfully" in captured.out

    def test_delete_principal_invalid_id(
        self, monkeypatch, dummy_principal_handler_obj, capsys
    ):
        monkeypatch.setattr(
            "src.controllers.handlers.principal_handler.validate.uuid_validator",
            lambda *args: "abc",
        )
        monkeypatch.setattr(
            dummy_principal_handler_obj, "get_all_active_pid", lambda *args: [("om",)]
        )
        dummy_principal_handler_obj.delete_principal()
        captured = capsys.readouterr()
        assert "\nNo such Principal Found\n" in captured.out

    def test_delete_principal_valid_id(
        self,
        monkeypatch,
        dummy_principal_handler_obj,
        set_mockeypatch_for_non_returning_query_without_error,
        capsys,
    ):
        monkeypatch.setattr(
            "src.controllers.handlers.principal_handler.validate.uuid_validator",
            lambda *args: "om",
        )
        monkeypatch.setattr(
            dummy_principal_handler_obj, "get_all_active_pid", lambda *args: [("om",)]
        )
        dummy_principal_handler_obj.delete_principal()
        captured = capsys.readouterr()
        assert "\nDeleted Successfully" in captured.out
