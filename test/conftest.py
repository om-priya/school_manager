# To mock whole db
import pytest
import sqlite3


@pytest.fixture
def mock_execute_returning_query_valid_data():
    def func_with_data(*args, **kwargs):
        return [("om", "Priya"), ("Shreyansh", "Agrawal")]

    return func_with_data


@pytest.fixture
def mock_execute_returning_query_no_data():
    def func_with_no_data(*args, **kwargs):
        return []

    return func_with_no_data


@pytest.fixture
def mock_execute_returning_query_with_error():
    def func_with_error(*args, **kwargs):
        raise sqlite3.Error

    return func_with_error


@pytest.fixture
def mock_execute_non_returning_query():
    def func_with_no_error(*args, **kwargs):
        pass

    return func_with_no_error


@pytest.fixture
def mock_execute_non_returning_query_with_error():
    def func_with_error(*args, **kwargs):
        raise sqlite3.Error

    return func_with_error
