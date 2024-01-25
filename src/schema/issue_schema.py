from marshmallow import fields, validate
from config.regex_pattern import RegexPatterns
from schema.config_schema import CustomSchema

class IssueSchema(CustomSchema):
    issue_message = fields.String(
        required=True, validate=validate.Regexp(RegexPatterns.MESSAGE_PATTERN)
    )