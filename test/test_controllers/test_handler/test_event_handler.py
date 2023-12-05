from src.controllers.handlers.event_handler import EventHandler
import pytest


# read event 1> data, nodata, error
@pytest.fixture
def dummy_event_handler_obj():
    dummy_obj = EventHandler("abc")
    return dummy_obj


class TestEventHandler:
    def test_read_event_with_data(
        self,
        monkeypatch,
        mock_execute_returning_query_valid_data,
        dummy_event_handler_obj,
        capsys,
    ):
        monkeypatch.setattr(
            "src.controllers.handlers.event_handler.DatabaseAccess.execute_returning_query",
            mock_execute_returning_query_valid_data,
        )
        dummy_event_handler_obj.read_event()
        captured = capsys.readouterr()
        assert "om" in captured.out

    def test_read_event_with_no_data(
        self,
        monkeypatch,
        mock_execute_returning_query_no_data,
        dummy_event_handler_obj,
        capsys,
    ):
        monkeypatch.setattr(
            "src.controllers.handlers.event_handler.DatabaseAccess.execute_returning_query",
            mock_execute_returning_query_no_data,
        )
        dummy_event_handler_obj.read_event()
        captured = capsys.readouterr()
        assert "\nNo such Notice Found\n" in captured.out

    def test_read_event_with_error(
        self,
        monkeypatch,
        mock_execute_non_returning_query_with_error,
        dummy_event_handler_obj,
        capsys,
    ):
        monkeypatch.setattr(
            "src.controllers.handlers.event_handler.DatabaseAccess.execute_returning_query",
            mock_execute_non_returning_query_with_error,
        )
        dummy_event_handler_obj.read_event()
        captured = capsys.readouterr()
        assert "Something went wrong with db: \n" in captured.out

    # testing for create_event function
    def test_create_event_with_no_error(
        self,
        monkeypatch,
        mock_execute_non_returning_query,
        dummy_event_handler_obj,
        capsys,
    ):
        monkeypatch.setattr(
            "src.controllers.handlers.event_handler.pattern_validator",
            lambda *args: "Demo Message for testing",
        )
        monkeypatch.setattr(
            "src.controllers.handlers.event_handler.DatabaseAccess.execute_non_returning_query",
            mock_execute_non_returning_query,
        )

        dummy_event_handler_obj.create_event()
        captured = capsys.readouterr()

        assert "\nNotice Added Successfully\n\n" in captured.out

    def test_create_event_with_error(
        self,
        monkeypatch,
        mock_execute_non_returning_query_with_error,
        dummy_event_handler_obj,
        capsys,
    ):
        monkeypatch.setattr(
            "src.controllers.handlers.event_handler.pattern_validator",
            lambda *args: "Demo Message for testing",
        )
        monkeypatch.setattr(
            "src.controllers.handlers.event_handler.DatabaseAccess.execute_non_returning_query",
            mock_execute_non_returning_query_with_error,
        )

        dummy_event_handler_obj.create_event()
        captured = capsys.readouterr()

        assert "Something went wrong with db: \n" in captured.out
