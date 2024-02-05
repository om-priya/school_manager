"""This module controls the login and signup functionality"""

import logging

from flask_jwt_extended import create_access_token
from flask_smorest import abort
from shortuuid import ShortUUID

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
            logger.info(f"{get_request_id()} calls the validation function")

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
                "User Logged In SuccessFully",
                {"access_token": access_token},
            ).get_json()
        except InvalidCredentials:
            logger.info(f"{get_request_id()} Invalid credentials is provided")
            return abort(
                401,
                message=ErrorResponse(
                    401, "Username or Passwrod is Incorrect"
                ).get_json(),
            )
        except NotActive:
            logger.info(f"{get_request_id()} User Not Approved")
            return abort(
                403,
                message=ErrorResponse(
                    403, "You Don't have access to the platform"
                ).get_json(),
            )
        except DataNotFound:
            logger.info(f"{get_request_id()} User No Longer Active/Deleted")
            return abort(404, message=ErrorResponse(404, "User Not Found").get_json())

    @staticmethod
    def sign_up_controller(user_info):
        """This function is responsible for signing up a user on the platform."""
        # Creating Object according to role and saving it
        try:
            AuthenticationHandler.sign_up(user_info)
            return SuccessResponse(
                200, "User Signed Up SuccessFully wait for Approval"
            ).get_json()
        except DataNotFound:
            return abort(
                404,
                message=ErrorResponse(
                    404, "No Such School present in the system"
                ).get_json(),
            )
        except DuplicateEntry:
            return abort(
                409,
                message=ErrorResponse(
                    409, "User Already Exists With Provided Info"
                ).get_json(),
            )

    @staticmethod
    def logout_controller():
        try:
            token_id = get_token_id_from_jwt()
            AuthenticationHandler.logout_handler(token_id)
            return SuccessResponse(200, "Log Out Successfully").get_json()
        except DuplicateEntry:
            logger.critical("Someone Tried to use blocklist token")
            return abort(
                409,
                message=ErrorResponse(
                    409, "User Already Exists With Provided Info"
                ).get_json(),
            )
