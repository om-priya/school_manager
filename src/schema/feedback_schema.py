from marshmallow import fields, validate
from config.regex_pattern import RegexPatterns
from schema.config_schema import CustomSchema

class FeedbackSchema(CustomSchema):
    feedback_message = fields.String(
        required=True, validate=validate.Regexp(RegexPatterns.MESSAGE_PATTERN)
    )


class FeedbackTeacherIdSchema(CustomSchema):
    teacher_id = fields.String(
        required=True, validate=validate.Regexp(RegexPatterns.UUID_PATTERN)
    )
