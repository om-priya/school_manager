import sqlite3
from src.utils.exception_handler import exception_checker

# check that whether exception is raising or not


def mock_sqlite_operational_func():
    raise sqlite3.OperationalError


def mock_sqlite_integrity_func():
    raise sqlite3.IntegrityError


def mock_sqlite_error_func():
    raise sqlite3.Error


def mock_value_error_func():
    raise ValueError


def mock_index_error_func():
    raise IndexError


def mock_generic_error_func():
    raise Exception


def mock_success_func():
    print("Success")


class TestExceptionChecker:
    def test_sqlite_operational_error(self, capsys):
        exception_checker(mock_sqlite_operational_func)()
        captured = capsys.readouterr()
        assert "kindly Check Your Query: " in captured.out

    def test_sqlite_integrity_error(self, capsys):
        exception_checker(mock_sqlite_integrity_func)()
        captured = capsys.readouterr()
        assert "Integrity Constraint Failed: " in captured.out

    def test_sqlite_error(self, capsys):
        exception_checker(mock_sqlite_error_func)()
        captured = capsys.readouterr()
        assert "Something went wrong with db: " in captured.out

    def test_value_error(self, capsys):
        exception_checker(mock_value_error_func)()
        captured = capsys.readouterr()
        assert "Wrong Value is provided" in captured.out

    def test_generic_error(self, capsys):
        exception_checker(mock_generic_error_func)()
        captured = capsys.readouterr()
        assert "Something Went Wrong: " in captured.out

    def test_index_error(self, capsys):
        exception_checker(mock_index_error_func)()
        captured = capsys.readouterr()
        assert "Something Went Wrong: " in captured.out

    def test_success_execution(self, capsys):
        exception_checker(mock_success_func)()
        captured = capsys.readouterr()
        assert "Success" in captured.out
