from marshmallow import fields, validate
from config.regex_pattern import RegexPatterns
from schema.config_schema import CustomSchema

class PrincipalIdSchema(CustomSchema):
    principal_id = fields.String(
        required=True, validate=validate.Regexp(RegexPatterns.UUID_PATTERN)
    )
