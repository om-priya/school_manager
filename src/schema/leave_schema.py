from marshmallow import fields, Schema, validate
from config.regex_pattern import RegexPatterns


class LeaveSchema(Schema):
    leave_date = fields.Date()
    no_of_daya = fields.String(required=True)


class LeaveIdSchema(Schema):
    leave_id = fields.String(
        required=True, validate=validate.Regexp(RegexPatterns.UUID_PATTERN)
    )
