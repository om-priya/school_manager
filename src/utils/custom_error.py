class DataNotFound(Exception):
    pass


class InvalidCredentials(Exception):
    pass


class NotActive(Exception):
    pass


class DuplicateEntry(Exception):
    pass


class AlreadyPresent(Exception):
    pass


class FailedAction(Exception):
    pass

class FailedValidation(Exception):
    def __init__(self, message):
        self.message = message
