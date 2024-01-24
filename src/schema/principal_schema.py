from marshmallow import fields, Schema, validate
from config.regex_pattern import RegexPatterns


class PrincipalIdSchema(Schema):
    principal_id = fields.String(
        required=True, validate=validate.Regexp(RegexPatterns.UUID_PATTERN)
    )
