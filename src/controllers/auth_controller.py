"""This module controls the login and signup functionality"""
import logging
from models.principals import Principal
from models.teachers import Teacher
from config.sqlite_queries import UserQueries
from database.database_access import DatabaseAccess
from utils import validate
from models.response_format import ErrorResponse, SuccessResponse
from datetime import timedelta
from flask_jwt_extended import create_access_token
from utils.hash_password import hash_password
from flask_smorest import abort
from utils.custom_error import (
    DataNotFound,
    InvalidCredentials,
    NotActive,
    DuplicateEntry,
)
from handlers.auth_handler import AuthenticationHandler

logger = logging.getLogger(__name__)


class AuthenticationController:
    @staticmethod
    def login_controller(login_details):
        """
        Check whether the user is valid or not.

        Returns:
        List: ['success': True/False, 'user_id': user_id, 'role': role]
        """
        try:
            user_details = AuthenticationHandler.is_logged_in(
                login_details["user_name"], login_details["password"]
            )
            access_token = create_access_token(
                identity={"user_id": user_details[1], "role": user_details[2]},
                expires_delta=timedelta(minutes=60)
            )
            return SuccessResponse(
                200,
                "User Logged In SuccessFully",
                {"access_token": access_token},
            ).get_json()
        except InvalidCredentials:
            return abort(
                401,
                message=ErrorResponse(
                    401, "Username or Passwrod is Incorrect"
                ).get_json(),
            )
        except NotActive:
            return abort(
                403,
                message=ErrorResponse(
                    403, "You Don't have access to the platform"
                ).get_json(),
            )
        except DataNotFound:
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
        except DuplicateEntry:
            return abort(
                409,
                message=ErrorResponse(
                    409, "User Already Exists With Provided Info"
                ).get_json(),
            )
