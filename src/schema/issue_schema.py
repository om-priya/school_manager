from marshmallow import fields, Schema, validate
from config.regex_pattern import RegexPatterns


class IssueSchema(Schema):
    issue_message = fields.String(
        required=True, validate=validate.Regexp(RegexPatterns.MESSAGE_PATTERN)
    )