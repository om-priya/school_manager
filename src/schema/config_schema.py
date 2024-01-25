from marshmallow import Schema, ValidationError
from utils.custom_error import FailedValidation


class CustomSchema(Schema):
    def handle_error(self, error, data, many, **kwargs):
        raise FailedValidation(error)
