from marshmallow import fields, Schema, validate
from config.regex_pattern import RegexPatterns


class ChangePasswordSchema(Schema):
    user_name = fields.String(
        required=True, validate=validate.Regexp(RegexPatterns.USERNAME_PATTERN)
    )
    password = fields.String(
        required=True, validate=validate.Regexp(RegexPatterns.PASSWORD_PATTERN)
    )
    new_password = fields.String(
        required=True, validate=validate.Regexp(RegexPatterns.PASSWORD_PATTERN)
    )
