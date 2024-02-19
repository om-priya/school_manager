"""This module controls the login and signup functionality"""

import logging

import mysql.connector
import pymysql

from models.principals import Principal, SavePrincipal
from models.teachers import Teacher, SaveTeacher
from config.sqlite_queries import UserQueries, CreateTable
from database.database_access import DatabaseAccess
from utils.hash_password import hash_password
from utils.custom_error import (
    DataNotFound,
    InvalidCredentials,
    NotActive,
    DuplicateEntry,
)
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
            raise InvalidCredentials
        elif data[0]["status"] == "pending":
            logger.error(
                f"{get_request_id()}Pending User %s tried to logged In",
                data[0]["user_id"],
            )
            raise NotActive
        elif data[0]["status"] == "deactivate":
            logger.error(f"{get_request_id()}User %s don't exists", data[0]["user_id"])
            raise DataNotFound
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
            raise DuplicateEntry from integrity_error

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
            raise DuplicateEntry from integrity_error
