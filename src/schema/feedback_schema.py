from marshmallow import fields, Schema, validate
from config.regex_pattern import RegexPatterns


class FeedbackSchema(Schema):
    feedback_message = fields.String(
        required=True, validate=validate.Regexp(RegexPatterns.MESSAGE_PATTERN)
    )


class FeedbackTeacherIdSchema(Schema):
    teacher_id = fields.String(
        required=True, validate=validate.Regexp(RegexPatterns.UUID_PATTERN)
    )
