"""This module controls the login and signup functionality"""
import logging
from models.principals import Principal
from models.teachers import Teacher
from config.display_menu import PromptMessage
from config.regex_pattern import RegexPatterns
from config.sqlite_queries import UserQueries
from database.database_access import DatabaseAccess
from utils import validate
from utils.hash_password import hash_password
from utils.custom_error import DataNotFound, InvalidCredentials, NotActive

logger = logging.getLogger(__name__)


class AuthenticationController:
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
            logger.error("Wrong Credentials")
            raise InvalidCredentials
        elif data[0][2] == "pending":
            logger.error("Pending User %s tried to logged In", data[0][0])
            raise NotActive
        elif data[0][2] == "deactivate":
            logger.error("User %s don't exists", data[0][0])
            raise DataNotFound
        else:
            return [True, data[0][0], data[0][1]]

    @staticmethod
    def sign_up(user_info):
        """This function is responsible for signing up a user on the platform."""
        
        # Creating Object according to role and saving it
        if user_info["role"] == "teacher":
            new_teacher = Teacher(user_info)
            logger.info("Initiating saving teacher")
            new_teacher.save_teacher()
        else:
            new_principal = Principal(user_info)
            logger.info("Initiating saving principal")
            new_principal.save_principal()
