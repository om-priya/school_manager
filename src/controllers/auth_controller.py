"""This module controls the login and signup functionality"""

import logging

from flask_jwt_extended import create_access_token
from flask_smorest import abort
from shortuuid import ShortUUID

from config.display_menu import PromptMessage
from models.response_format import ErrorResponse, SuccessResponse
from utils.custom_error import (
    DataNotFound,
    InvalidCredentials,
    NotActive,
    DuplicateEntry,
)
from handlers.auth_handler import AuthenticationHandler
from helper.helper_function import get_request_id, get_token_id_from_jwt

logger = logging.getLogger(__name__)


class AuthenticationController:
    """Controller for auth router"""

    @staticmethod
    def login_controller(login_details):
        """
        formatting data for different scenario while
        request is on /login
        """
        try:
            logger.info("%s calls the validation function", get_request_id())

            user_details = AuthenticationHandler.is_logged_in(
                login_details["user_name"], login_details["password"]
            )

            logger.info(f"{get_request_id()} successfully validated")
            token_identifier = {"token_id": ShortUUID().random(length=10)}
            access_token = create_access_token(
                identity={"user_id": user_details[1], "role": user_details[2]},
                additional_claims=token_identifier,
            )

            logger.info(f"{get_request_id()} jwt token is generated and returned")
            return SuccessResponse(
                200,
                PromptMessage.SUCCESS_ACTION.format("User Logged In"),
                {"access_token": access_token},
            ).get_json()
        except InvalidCredentials:
            logger.error(f"{get_request_id()} Invalid credentials is provided")
            return abort(
                401,
                message=ErrorResponse(
                    401, PromptMessage.INCORRECT_CREDENTIALS
                ).get_json(),
            )
        except NotActive:
            logger.error(f"{get_request_id()} User Not Approved")
            return abort(
                403,
                message=ErrorResponse(
                    403, PromptMessage.DENIED_ACCESS.format("Platform")
                ).get_json(),
            )
        except DataNotFound:
            logger.error(f"{get_request_id()} User No Longer Active/Deleted")
            return abort(
                404,
                message=ErrorResponse(
                    404, PromptMessage.NOTHING_FOUND.format("User")
                ).get_json(),
            )

    @staticmethod
    def sign_up_controller(user_info):
        """This function is responsible for signing up a user on the platform."""
        # Creating Object according to role and saving it
        try:
            AuthenticationHandler.sign_up(user_info)
            logger.info(f"{get_request_id()} Signed Up Successfully")
            return SuccessResponse(201, PromptMessage.SIGNED_UP_SUCCESS).get_json()
        except DataNotFound:
            logger.error(f"{get_request_id()} Wrong School Name Provided")
            return abort(
                404,
                message=ErrorResponse(
                    404, PromptMessage.NOTHING_FOUND.format("School")
                ).get_json(),
            )
        except DuplicateEntry:
            logger.error(f"{get_request_id()} Duplicate Credentials Provided")
            return abort(
                409,
                message=ErrorResponse(409, PromptMessage.DUPLICATE_ENTRY).get_json(),
            )

    @staticmethod
    def logout_controller():
        """Controller for /logout endpoint"""
        try:
            token_id = get_token_id_from_jwt()
            logger.info(
                f"{get_request_id()} token fetched from jwt and called logout handler"
            )
            AuthenticationHandler.logout_handler(token_id)
            return SuccessResponse(200, PromptMessage.LOGGED_OUT).get_json()
        except DuplicateEntry:
            logger.critical(f"{get_request_id()} Someone Tried to use blocklist token")
            return abort(
                409,
                message=ErrorResponse(409, PromptMessage.DUPLICATE_ENTRY).get_json(),
            )
