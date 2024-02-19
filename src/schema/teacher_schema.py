from marshmallow import fields, validate
from config.regex_pattern import RegexPatterns
from schema.config_schema import CustomSchema


class TeacherIdSchema(CustomSchema):
    teacher_id = fields.String(
        required=True, validate=validate.Regexp(RegexPatterns.UUID_PATTERN)
    )


class TeacherDetails(CustomSchema):
    name = fields.String(
        required=True, validate=validate.Regexp(RegexPatterns.NAME_PATTERN)
    )
    gender = fields.String(
        required=True, validate=validate.Regexp(RegexPatterns.GENDER_PATTERN)
    )
    email = fields.String(
        required=True, validate=validate.Regexp(RegexPatterns.EMAIL_PATTERN)
    )
    phone = fields.String(
        required=True, validate=validate.Regexp(RegexPatterns.PHONE_PATTERN)
    )
