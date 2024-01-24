from marshmallow import fields, Schema, validate
from config.regex_pattern import RegexPatterns


class TeacherIdSchema(Schema):
    teacher_id = fields.String(
        required=True, validate=validate.Regexp(RegexPatterns.UUID_PATTERN)
    )
