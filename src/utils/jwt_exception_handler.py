"""
This file will handle all the
erros/exception for jwt
"""

import logging
from flask_jwt_extended import JWTManager
from models.response_format import ErrorResponse
from config.display_menu import PromptMessage
from helper.helper_function import get_request_id

logger = logging.getLogger(__name__)


def jwt_exception_manager(app):
    # create jwtmanager instance which will handle all the jwt related logic
    jwt = JWTManager(app)

    @jwt.revoked_token_loader
    def revoked_token_callback(_jwt_header, _jwt_payload):
        logger.warning(f"{get_request_id()} token is revoked")
        return (
            ErrorResponse(
                401, PromptMessage.TOKEN_RESPONSE.format("Revoked")
            ).get_json(),
            401,
        )

    @jwt.expired_token_loader
    def expired_token_callback(_jwt_header, _jwt_payload):
        logger.warning(f"{get_request_id()} token is expired")
        return (
            ErrorResponse(
                401, PromptMessage.TOKEN_RESPONSE.format("Not Valid")
            ).get_json(),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(_error):
        logger.warning(f"{get_request_id()} token is missing")
        return (
            ErrorResponse(
                401, PromptMessage.TOKEN_RESPONSE.format("Missing")
            ).get_json(),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(_error):
        logger.warning(f"{get_request_id()} token is invalid")
        return (
            ErrorResponse(
                401, PromptMessage.TOKEN_RESPONSE.format("Invalid")
            ).get_json(),
            401,
        )

    return app
