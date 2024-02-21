"""This module controls the login and signup functionality"""

import logging
import pymysql

from models.principals import Principal, SavePrincipal
from models.teachers import Teacher, SaveTeacher
from config.display_menu import PromptMessage
from config.sqlite_queries import UserQueries, CreateTable
from config.http_status_code import HttpStatusCode
from database.database_access import DatabaseAccess
from utils.hash_password import hash_password
from utils.custom_error import ApplicationError, DbException
from helper.helper_function import get_request_id


logger = logging.getLogger(__name__)


class AuthenticationHandler:
    """
    This class handles the buisness logic for login and signup
    """

    @staticmethod
    def is_logged_in(username, password):
        """
        Check whether the user is valid or not.

        Returns:
        List: ['success': True/False, 'user_id': user_id, 'role': role]
        """
        hashed_password = hash_password(password)

        # checking in db with username and password
        params = (username, hashed_password)
        data = DatabaseAccess.execute_returning_query(
            UserQueries.FETCH_FROM_CREDENTIALS, params
        )
        # Checking For Credentials with db response
        if len(data) == 0:
            logger.error(f"{get_request_id()} Wrong Credentials")
            raise ApplicationError(
                HttpStatusCode.UNAUTHORIZE, PromptMessage.INCORRECT_CREDENTIALS
            )
        elif data[0]["status"] == "pending":
            logger.error(
                f"{get_request_id()}Pending User %s tried to logged In",
                data[0]["user_id"],
            )
            raise ApplicationError(
                HttpStatusCode.FORBIDDEN, PromptMessage.DENIED_ACCESS.format("Platform")
            )
        elif data[0]["status"] == "deactivate":
            logger.error(f"{get_request_id()}User %s don't exists", data[0]["user_id"])
            raise ApplicationError(
                HttpStatusCode.NOT_FOUND, PromptMessage.NOTHING_FOUND.format("User")
            )
        else:
            logger.error(f"{get_request_id()}User %s Logged In", data[0]["user_id"])
            return [True, data[0]["user_id"], data[0]["role"]]

    @staticmethod
    def sign_up(user_info):
        """This function is responsible for signing up a user on the platform."""

        # Creating Object according to role and saving it
        try:
            if user_info["role"] == "teacher":
                new_teacher = Teacher(user_info)
                logger.info(f"{get_request_id()} Initiating saving teacher")
                SaveTeacher().save_teacher(new_teacher)
            else:
                new_principal = Principal(user_info)
                logger.info(f"{get_request_id()} Initiating saving principal")
                SavePrincipal().save_principal(new_principal)
        except pymysql.IntegrityError as integrity_error:
            logger.error(f"{get_request_id()} Integrity Error {integrity_error}")
            raise DbException(
                HttpStatusCode.CONFLICT, PromptMessage.DUPLICATE_ENTRY
            ) from integrity_error

    @staticmethod
    def logout_handler(token_id):
        try:
            logger.info(f"{get_request_id()} Saving token ID to db")
            DatabaseAccess.execute_non_returning_query(CreateTable.CREATE_TOKEN_TABLE)
            DatabaseAccess.execute_non_returning_query(
                CreateTable.INSERT_INTO_TOKEN, (token_id,)
            )
        except pymysql.IntegrityError as integrity_error:
            logger.error(f"{get_request_id()} Integrity Error {integrity_error}")
            raise DbException(
                HttpStatusCode.CONFLICT,
                PromptMessage.TOKEN_RESPONSE.format("already Invalid"),
            ) from integrity_error
