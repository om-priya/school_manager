"""This file will test all the function which are present in src.controllers.helper.helper_function"""

from src.controllers.helper.helper_function import (
    check_empty_data,
    fetch_salary_history,
    view_personal_info,
    change_password,
)
import pytest
import sqlite3

# testing check_empty_data function


def test_check_empty_data_valid_res_data():
    valid_res_data = [("Om", "Priya"), ("Abhay", "Agrawal"), ("Millind", "Bhatnagar")]
    actual_result = check_empty_data(valid_res_data, "")

    assert not actual_result


def test_check_empty_data_invalid_res_data():
    invalid_res_data = []
    actual_result = check_empty_data(invalid_res_data, "")

    assert actual_result


# testing fetch_salary_history function


def test_fetch_salary_history_with_data(
    monkeypatch, mock_execute_returning_query_valid_data, capsys
):
    monkeypatch.setattr(
        "src.controllers.helper.helper_function.DatabaseAccess.execute_returning_query",
        mock_execute_returning_query_valid_data,
    )
    fetch_salary_history("")
    captured = capsys.readouterr()

    assert "om" in captured.out


def test_fetch_salary_history_with_no_data(
    monkeypatch, mock_execute_returning_query_no_data, capsys
):
    monkeypatch.setattr(
        "src.controllers.helper.helper_function.DatabaseAccess.execute_returning_query",
        mock_execute_returning_query_no_data,
    )
    fetch_salary_history("")
    captured = capsys.readouterr()

    assert "\nNo such Salary History Found\n\n" in captured.out


def test_fetch_salary_history_with_error(
    monkeypatch, mock_execute_returning_query_with_error
):
    monkeypatch.setattr(
        "src.controllers.helper.helper_function.DatabaseAccess.execute_returning_query",
        mock_execute_returning_query_with_error,
    )
    with pytest.raises(sqlite3.Error):
        fetch_salary_history("")


# testing view_personal_info


def test_view_personal_info_with_data(
    monkeypatch, mock_execute_returning_query_valid_data, capsys
):
    monkeypatch.setattr(
        "src.controllers.helper.helper_function.DatabaseAccess.execute_returning_query",
        mock_execute_returning_query_valid_data,
    )
    view_personal_info("", "")
    captured = capsys.readouterr()

    assert "om" in captured.out


def test_view_personal_info_with_error(
    monkeypatch, mock_execute_returning_query_with_error
):
    monkeypatch.setattr(
        "src.controllers.helper.helper_function.DatabaseAccess.execute_returning_query",
        mock_execute_returning_query_with_error,
    )
    with pytest.raises(sqlite3.Error):
        view_personal_info("", "")


# test change_password function
def test_change_password_valid_cred(
    monkeypatch,
    mock_execute_returning_query_valid_data,
    mock_execute_non_returning_query,
    capsys,
):
    password_list = ["Ompriya@123", "Manipal@123"]
    monkeypatch.setattr(
        "src.controllers.helper.helper_function.validate.pattern_validator",
        lambda *args: "ompriya18153789",
    )
    monkeypatch.setattr(
        "src.controllers.helper.helper_function.validate.password_validator",
        lambda *args: password_list.pop(0),
    )
    monkeypatch.setattr(
        "src.controllers.helper.helper_function.DatabaseAccess.execute_returning_query",
        mock_execute_returning_query_valid_data,
    )
    monkeypatch.setattr(
        "src.controllers.helper.helper_function.DatabaseAccess.execute_non_returning_query",
        mock_execute_non_returning_query,
    )

    change_password("")
    captured = capsys.readouterr()
    assert "Password Updated Successfully" in captured.out


def test_change_password_invalid_cred(
    monkeypatch,
    mock_execute_returning_query_no_data,
    capsys,
):
    password_list = ["Ompriya@123"]
    monkeypatch.setattr(
        "src.controllers.helper.helper_function.validate.pattern_validator",
        lambda *args: "ompriya18153789",
    )
    monkeypatch.setattr(
        "src.controllers.helper.helper_function.validate.password_validator",
        lambda *args: password_list.pop(0),
    )
    monkeypatch.setattr(
        "src.controllers.helper.helper_function.DatabaseAccess.execute_returning_query",
        mock_execute_returning_query_no_data,
    )

    change_password("")
    captured = capsys.readouterr()
    assert "\nWrong Credentials" in captured.out
