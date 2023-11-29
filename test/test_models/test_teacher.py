from src.models.teachers import Teacher
import pytest


@pytest.fixture
def dummy_teacher_obj():
    teacher_info = {
        "name": "Om Priya",
        "gender": "M",
        "email": "ompriya18153789@gmail.com",
        "phone": "8229070126",
        "school_name": "dav public school",
        "experience": "2",
        "fav_subject": "pyhton",
        "role": "teacher",
        "password": "Ompriya@123",
    }
    dummy_obj = Teacher(teacher_info)
    return dummy_obj


def test_save_teacher_invalid_school_name(
    monkeypatch, mock_execute_returning_query_no_data, dummy_teacher_obj, capsys
):
    monkeypatch.setattr(
        "src.models.teachers.DatabaseAccess.execute_returning_query",
        mock_execute_returning_query_no_data,
    )
    dummy_teacher_obj.save_teacher()
    captured = capsys.readouterr()

    assert "\nWrong School Or School is not in the system" in captured.out


def test_save_teacher_valid_school_name(
    monkeypatch,
    mock_execute_returning_query_valid_data,
    dummy_teacher_obj,
    mock_database_connection,
    capsys,
):
    monkeypatch.setattr(
        "src.models.teachers.DatabaseAccess.execute_returning_query",
        mock_execute_returning_query_valid_data,
    )
    monkeypatch.setattr(
        "src.models.teachers.DatabaseConnection", mock_database_connection
    )
    dummy_teacher_obj.save_teacher()

    captured = capsys.readouterr()
    assert (
        "\nSigned Up Successfully Wait for Super Admin to approve it." in captured.out
    )
