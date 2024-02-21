"""Custom Error Classes for handling API failures"""


class ApplicationError(Exception):
    """Will throw application error"""

    def __init__(self, code, err_message):
        self.code = code
        self.err_message = err_message


class DbException(Exception):
    def __init__(self, code, err_message):
        self.code = code
        self.err_message = err_message


class FailedValidation(Exception):
    """To handle validation error of marshmallow"""

    def __init__(self, message):
        self.message = message
