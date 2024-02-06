"""
This file handles the functionality for the user
which are shared between all roles
"""

import logging
from config.display_menu import PromptMessage
from config.sqlite_queries import UserQueries, CreateTable
from database.database_access import DatabaseAccess
from utils.hash_password import hash_password
from utils.custom_error import FailedAction, DataNotFound, InvalidCredentials
from handlers.principal_handler import PrincipalHandler
from handlers.teacher_handler import TeacherHandler
from helper.helper_function import get_request_id, get_token_id_from_jwt


logger = logging.getLogger(__name__)


def fetch_salary_history(user_id):
    """Fetching salary history of a particular user"""
    logger.info(f"{get_request_id()} Fetching Salary History for user - {user_id}")
    res_data = DatabaseAccess.execute_returning_query(
        UserQueries.GET_SALARY_HISTORY, (user_id,)
    )

    # if there is no any records for a teacher
    if len(res_data) == 0:
        logger.error(f"{get_request_id()} No Salary History Found")
        raise DataNotFound

    logger.info(f"{get_request_id()} Returning Salary History for user - {user_id}")
    return res_data


def view_personal_info(role, user_id):
    """This function will print a user profile"""
    if role == "principal":
        res_data = PrincipalHandler().get_principal_by_id(user_id)
    elif role == "teacher":
        res_data = TeacherHandler().get_teacher_by_id(user_id)
    else:
        raise FailedAction

    return res_data


def change_password_handler(user_id, username, password, new_password):
    """This function can change the password of user"""
    hashed_password = hash_password(password)

    # checking in db with username and password
    logger.info(
        f"{get_request_id()} fetching from cred table with username and hashed password"
    )
    params = (username, hashed_password, user_id)
    res_data = DatabaseAccess.execute_returning_query(
        UserQueries.CHECK_USER_EXIST, params
    )

    if len(res_data) == 0:
        logger.error(f"{get_request_id()} Wrong Credentials")
        raise InvalidCredentials

    hashed_new_password = hash_password(new_password)

    # update new password to db
    logger.info(f"Changing password for user - {user_id}")
    params = (hashed_new_password, user_id)
    DatabaseAccess.execute_non_returning_query(
        UserQueries.CHANGE_PASSWORD_QUERY, params
    )
    logger.info(f"Blocklisting token - {user_id}")
    token_id = get_token_id_from_jwt()
    DatabaseAccess.execute_non_returning_query(CreateTable.CREATE_TOKEN_TABLE)
    DatabaseAccess.execute_non_returning_query(
        CreateTable.INSERT_INTO_TOKEN, (token_id,)
    )
    logger.info(
        f"Password Changed for user {user_id} and token is blocked with token_id {token_id}"
    )
