from marshmallow import fields, validate, validates_schema, ValidationError
from config.regex_pattern import RegexPatterns
from datetime import datetime
from schema.config_schema import CustomSchema

class LeaveSchema(CustomSchema):
    leave_date = fields.String(required=True)
    no_of_days = fields.String(required=True)

    @validates_schema
    def validate_date(self, data, **kwargs):
        try:
            date_str = data["leave_date"]
            start_date = datetime.strptime(date_str, "%d-%m-%Y").date()
            if start_date > datetime.now().date():
                return start_date
            elif start_date <= datetime.now().date():
                raise ValueError
        except ValueError:
            raise ValidationError(message="Date Format Is Wrong")


class LeaveIdSchema(CustomSchema):
    leave_id = fields.String(
        required=True, validate=validate.Regexp(RegexPatterns.UUID_PATTERN)
    )
