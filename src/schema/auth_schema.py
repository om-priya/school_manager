from marshmallow import fields, Schema, validate, validates_schema, ValidationError
from config.regex_pattern import RegexPatterns

from schema.config_schema import CustomSchema


class SignUpSchema(CustomSchema):
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
    school_name = fields.String(
        required=True, validate=validate.Regexp(RegexPatterns.SCHOOL_NAME_PATTERN)
    )
    password = fields.String(
        required=True, validate=validate.Regexp(RegexPatterns.PASSWORD_PATTERN)
    )
    role = fields.String(
        required=True, validate=validate.Regexp(RegexPatterns.ROLE_PATTERN)
    )
    experience = fields.String(
        required=True, validate=validate.Regexp(RegexPatterns.EXPERIENCE_PATTERN)
    )
    fav_subject = fields.String(
        validate=validate.Regexp(RegexPatterns.FAV_SUBJECT_PATTERN)
    )

    @validates_schema
    def validate_fav_subject(self, data, **kwargs):
        if data["role"] == "teacher" and data.get("fav_subject") == None:
            raise ValidationError("Fav_Subject Didn't Provided")


class LoginSchema(CustomSchema):
    user_name = fields.String(
        required=True, validate=validate.Regexp(RegexPatterns.USERNAME_PATTERN)
    )
    password = fields.String(
        required=True, validate=validate.Regexp(RegexPatterns.PASSWORD_PATTERN)
    )
