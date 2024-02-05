"""
This file will handle all the
erros/exception for jwt
"""

from flask_jwt_extended import JWTManager
from models.response_format import ErrorResponse
from config.display_menu import PromptMessage


def jwt_exception_manager(app):
    # create jwtmanager instance which will handle all the jwt related logic
    jwt = JWTManager(app)

    # custom errors for jwt failure
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(_jwt_header, _jwt_payload):
        pass

    @jwt.revoked_token_loader
    def revoked_token_callback(_jwt_header, _jwt_payload):
        return (
            ErrorResponse(
                401, PromptMessage.TOKEN_RESPONSE.format("Revoked")
            ).get_json(),
            401,
        )

    @jwt.expired_token_loader
    def expired_token_callback(_jwt_header, _jwt_payload):
        return (
            ErrorResponse(
                401, PromptMessage.TOKEN_RESPONSE.format("Not Valid")
            ).get_json(),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(_error):
        return (
            ErrorResponse(
                401, PromptMessage.TOKEN_RESPONSE.format("Missing")
            ).get_json(),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(_error):
        return (
            ErrorResponse(
                401, PromptMessage.TOKEN_RESPONSE.format("Invalid")
            ).get_json(),
            401,
        )

    return app
