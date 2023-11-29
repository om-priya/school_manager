from src.controllers.handlers.feedback_handler import FeedbackHandler
import pytest


def mock_pretty_print():
    print("")


@pytest.fixture
def dummy_feedback_handler_obj():
    dummy_obj = FeedbackHandler("abc")
    return dummy_obj


# testing read_
def test_read_feedback_with_data(
    monkeypatch,
    mock_execute_returning_query_valid_data,
    dummy_feedback_handler_obj,
    capsys,
):
    monkeypatch.setattr(
        "src.controllers.handlers.feedback_handler.DatabaseAccess.execute_returning_query",
        mock_execute_returning_query_valid_data,
    )
    dummy_feedback_handler_obj.read_feedback()
    captured = capsys.readouterr()
    assert "om" in captured.out


def test_read_feedback_with_no_data(
    monkeypatch,
    mock_execute_returning_query_no_data,
    dummy_feedback_handler_obj,
    capsys,
):
    monkeypatch.setattr(
        "src.controllers.handlers.feedback_handler.DatabaseAccess.execute_returning_query",
        mock_execute_returning_query_no_data,
    )
    dummy_feedback_handler_obj.read_feedback()
    captured = capsys.readouterr()
    assert "\nNo such FeedBack Found\n\n" in captured.out


def test_read_feedback_with_error(
    monkeypatch,
    mock_execute_returning_query_with_error,
    dummy_feedback_handler_obj,
    capsys,
):
    monkeypatch.setattr(
        "src.controllers.handlers.feedback_handler.DatabaseAccess.execute_returning_query",
        mock_execute_returning_query_with_error,
    )
    dummy_feedback_handler_obj.read_feedback()
    captured = capsys.readouterr()
    assert "Something went wrong with db: \n" in captured.out


def test_give_feedback_with_no_teacher(
    monkeypatch,
    mock_execute_returning_query_no_data,
    dummy_feedback_handler_obj,
    capsys,
):
    monkeypatch.setattr(
        "src.controllers.handlers.feedback_handler.DatabaseAccess.execute_returning_query",
        mock_execute_returning_query_no_data,
    )

    dummy_feedback_handler_obj.give_feedback()
    captured = capsys.readouterr()

    assert "\nNo such Teacher Found\n" in captured.out


def test_give_feedback_with_error(
    monkeypatch,
    mock_execute_returning_query_with_error,
    dummy_feedback_handler_obj,
    capsys,
):
    monkeypatch.setattr(
        "src.controllers.handlers.feedback_handler.DatabaseAccess.execute_returning_query",
        mock_execute_returning_query_with_error,
    )
    dummy_feedback_handler_obj.give_feedback()
    captured = capsys.readouterr()

    assert "Something went wrong with db: \n" in captured.out


def test_give_feedback_with_invalid_teacher_id(
    monkeypatch,
    mock_execute_returning_query_valid_data,
    dummy_feedback_handler_obj,
    capsys,
):
    monkeypatch.setattr(
        "src.controllers.handlers.feedback_handler.DatabaseAccess.execute_returning_query",
        mock_execute_returning_query_valid_data,
    )
    monkeypatch.setattr(
        "src.controllers.handlers.feedback_handler.uuid_validator",
        lambda *args: "Millind",
    )

    dummy_feedback_handler_obj.give_feedback()
    captured = capsys.readouterr()

    assert "\nNo such Teacher Found\n" in captured.out


def test_give_feedback_with_valid_teacher_id(
    monkeypatch,
    mock_execute_returning_query_valid_data,
    mock_execute_non_returning_query,
    dummy_feedback_handler_obj,
    capsys,
):
    monkeypatch.setattr(
        "src.controllers.handlers.feedback_handler.DatabaseAccess.execute_returning_query",
        mock_execute_returning_query_valid_data,
    )
    monkeypatch.setattr(
        "src.controllers.handlers.feedback_handler.uuid_validator",
        lambda *args: "om",
    )
    monkeypatch.setattr(
        "src.controllers.handlers.feedback_handler.pattern_validator",
        lambda *args: "Demo Feedback",
    )
    monkeypatch.setattr(
        "src.controllers.handlers.feedback_handler.pretty_print",
        lambda *args, **kwargs: mock_pretty_print,
    )
    monkeypatch.setattr(
        "src.controllers.handlers.feedback_handler.DatabaseAccess.execute_non_returning_query",
        mock_execute_non_returning_query,
    )

    dummy_feedback_handler_obj.give_feedback()
    captured = capsys.readouterr()
    print(captured)
    assert "\nFeedbacks Added Successfully\n\n" in captured.out
