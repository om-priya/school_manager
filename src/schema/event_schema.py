from marshmallow import fields, validate
from config.regex_pattern import RegexPatterns
from schema.config_schema import CustomSchema


class EventSchema(CustomSchema):
    event_message = fields.String(
        required=True, validate=validate.Regexp(RegexPatterns.MESSAGE_PATTERN)
    )
