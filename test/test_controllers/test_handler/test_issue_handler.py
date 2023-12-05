import pytest
from src.controllers.handlers.issue_handler import IssueHandler


@pytest.fixture
def dummy_issue_handler_obj():
    dummy_obj = IssueHandler("abc")
    return dummy_obj


class TestIssueHandler:
    # testing view_issue
    def test_view_issue_with_data(
        self,
        monkeypatch,
        mock_execute_returning_query_valid_data,
        dummy_issue_handler_obj,
        capsys,
    ):
        monkeypatch.setattr(
            "src.controllers.handlers.issue_handler.DatabaseAccess.execute_returning_query",
            mock_execute_returning_query_valid_data,
        )
        dummy_issue_handler_obj.view_issue()
        captured = capsys.readouterr()
        assert "om" in captured.out

    def test_view_issue_with_no_data(
        self,
        monkeypatch,
        mock_execute_returning_query_no_data,
        dummy_issue_handler_obj,
        capsys,
    ):
        monkeypatch.setattr(
            "src.controllers.handlers.issue_handler.DatabaseAccess.execute_returning_query",
            mock_execute_returning_query_no_data,
        )
        dummy_issue_handler_obj.view_issue()
        captured = capsys.readouterr()
        assert "\nNo such Issues Found\n" in captured.out

    def test_view_issue_with_error(
        self,
        monkeypatch,
        mock_execute_returning_query_with_error,
        dummy_issue_handler_obj,
        capsys,
    ):
        monkeypatch.setattr(
            "src.controllers.handlers.issue_handler.DatabaseAccess.execute_returning_query",
            mock_execute_returning_query_with_error,
        )
        dummy_issue_handler_obj.view_issue()
        captured = capsys.readouterr()
        assert "Something went wrong with db: \n" in captured.out

    # testing raise_issue
    def test_raise_issue_with_no_error(
        self,
        monkeypatch,
        mock_execute_non_returning_query,
        dummy_issue_handler_obj,
        capsys,
    ):
        monkeypatch.setattr(
            "src.controllers.handlers.issue_handler.pattern_validator",
            lambda *args: "Demo Issue",
        )
        monkeypatch.setattr(
            "src.controllers.handlers.issue_handler.DatabaseAccess.execute_non_returning_query",
            mock_execute_non_returning_query,
        )

        dummy_issue_handler_obj.raise_issue()
        captured = capsys.readouterr()

        assert "\nIssue Added Successfully\n" in captured.out

    def test_raise_issue_with_error(
        self,
        monkeypatch,
        mock_execute_non_returning_query_with_error,
        dummy_issue_handler_obj,
        capsys,
    ):
        monkeypatch.setattr(
            "src.controllers.handlers.issue_handler.pattern_validator",
            lambda *args: "Demo Issue",
        )
        monkeypatch.setattr(
            "src.controllers.handlers.issue_handler.DatabaseAccess.execute_non_returning_query",
            mock_execute_non_returning_query_with_error,
        )

        dummy_issue_handler_obj.raise_issue()
        captured = capsys.readouterr()

        assert "Something went wrong with db: \n" in captured.out
