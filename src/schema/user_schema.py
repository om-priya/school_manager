from marshmallow import fields, validate
from config.regex_pattern import RegexPatterns
from schema.config_schema import CustomSchema


class ChangePasswordSchema(CustomSchema):
    user_name = fields.String(
        required=True, validate=validate.Regexp(RegexPatterns.USERNAME_PATTERN)
    )
    password = fields.String(
        required=True, validate=validate.Regexp(RegexPatterns.PASSWORD_PATTERN)
    )
    new_password = fields.String(
        required=True, validate=validate.Regexp(RegexPatterns.PASSWORD_PATTERN)
    )
