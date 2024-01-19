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

logger = logging.getLogger(__name__)


class AuthenticationController:
    @staticmethod
    def is_logged_in():
        """
        Check whether the user is valid or not.

        Returns:
        List: ['success': True/False, 'user_id': user_id, 'role': role]
        """
        # Taking Username and password and validating it
        username = validate.pattern_validator(
            PromptMessage.TAKE_INPUT.format("Username"), RegexPatterns.USERNAME_PATTERN
        )
        password = validate.password_validator()
        hashed_password = hash_password(password)

        # checking in db with username and password
        params = (username, hashed_password)
        data = DatabaseAccess.execute_returning_query(
            UserQueries.FETCH_FROM_CREDENTIALS, params
        )

        # Checking For Credentials with db response
        if len(data) == 0:
            logger.error("Wrong Credentials")
            print(PromptMessage.WRONG_CREDENTIALS)
        elif data[0][2] == "pending":
            logger.error("Pending User %s tried to logged In", data[0][0])
            print(PromptMessage.PENDING_USER_LOG_IN)
        elif data[0][2] == "deactivate":
            logger.error("User %s don't exists", data[0][0])
            print(PromptMessage.NOTHING_FOUND.format("User"))
        else:
            return [True, data[0][0], data[0][1]]

        return [False, "", ""]

    @staticmethod
    def sign_up():
        """This function is responsible for signing up a user on the platform."""
        print(PromptMessage.GREET_PROMPT.format("User"))
        print("\n")

        # Taking User Input For SignUp with Validations
        user_info = {}
        user_info["name"] = validate.pattern_validator(
            PromptMessage.TAKE_INPUT.format("Name"), RegexPatterns.NAME_PATTERN
        )
        user_info["gender"] = validate.pattern_validator(
            PromptMessage.TAKE_INPUT.format("Gender (M/F)"),
            RegexPatterns.GENDER_PATTERN,
        )
        user_info["email"] = validate.pattern_validator(
            PromptMessage.TAKE_INPUT.format("email"), RegexPatterns.EMAIL_PATTERN
        )
        user_info["phone"] = validate.pattern_validator(
            PromptMessage.TAKE_INPUT.format("Phone Number"), RegexPatterns.PHONE_PATTERN
        )
        user_info["school_name"] = validate.pattern_validator(
            PromptMessage.TAKE_INPUT.format("School Name (only dav public school)"),
            RegexPatterns.SCHOOL_NAME_PATTERN,
        )
        user_info["password"] = validate.password_validator()
        user_info["role"] = validate.pattern_validator(
            PromptMessage.TAKE_INPUT.format("Role (teacher,principal)"),
            RegexPatterns.ROLE_PATTERN,
        )
        user_info["experience"] = validate.pattern_validator(
            PromptMessage.TAKE_INPUT.format("Experience in Year"),
            RegexPatterns.EXPERIENCE_PATTERN,
        )

        # Creating Object according to role and saving it
        if user_info["role"] == "teacher":
            user_info["fav_subject"] = validate.pattern_validator(
                PromptMessage.TAKE_INPUT.format("Fav Subject"),
                RegexPatterns.FAV_SUBJECT_PATTERN,
            )
            new_teacher = Teacher(user_info)
            logger.info("Initiating saving teacher")
            new_teacher.save_teacher()
        else:
            new_principal = Principal(user_info)
            logger.info("Initiating saving principal")
            new_principal.save_principal()
