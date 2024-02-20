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


class DataNotFound(Exception):
    """No resouce found"""


class InvalidCredentials(Exception):
    """Invalid cred provided"""


class NotActive(Exception):
    """User no longer active"""


class DuplicateEntry(Exception):
    """Already present in db"""


class AlreadyPresent(Exception):
    """Already present in system"""


class FailedAction(Exception):
    """Can't perform action for this request"""


class FailedValidation(Exception):
    """To handle validation error of marshmallow"""

    def __init__(self, message):
        self.message = message
