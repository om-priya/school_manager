"""This file contains some helper function which are used for multiple controllers"""

import logging
from src.config.display_menu import PromptMessage
from src.config.sqlite_queries import UserQueries
from src.config.regex_pattern import RegexPatterns
from src.config.headers_for_output import TableHeaders
from src.database import database_access as DAO
from src.utils.pretty_print import pretty_print
from src.utils.hash_password import hash_password
from src.utils import validate

logger = logging.getLogger(__name__)


def fetch_salary_history(user_id):
    """Fetching salary history of a particular user"""
    res_data = DAO.execute_returning_query(UserQueries.GET_SALARY_HISTORY, (user_id,))

    # if there is no any records for a teacher
    if len(res_data) == 0:
        logger.error("No Salary History Found")
        print(PromptMessage.NOTHING_FOUND.format("Salary History"))
        return

    headers = (
        TableHeaders.ID.format("Salary"),
        TableHeaders.YEAR,
        TableHeaders.MONTH,
        TableHeaders.AMOUNT,
        TableHeaders.PAY_DATE,
    )
    pretty_print(res_data, headers)


def view_personal_info(query, user_id):
    """This function will print a user profile"""
    res_data = DAO.execute_returning_query(query, (user_id,))

    # info for logged in user
    headers = (
        TableHeaders.ID.format("User"),
        TableHeaders.NAME,
        TableHeaders.PHONE,
        TableHeaders.EMAIL,
        TableHeaders.STATUS,
    )
    pretty_print(res_data, headers)


def change_password(user_id):
    """This function can change the password of user"""
    username = validate.pattern_validator(
        PromptMessage.TAKE_INPUT.format("Username"), RegexPatterns.USERNAME_PATTERN
    )
    password = validate.password_validator()
    hashed_password = hash_password(password)

    # checking in db with username and password
    params = (username, hashed_password, user_id)
    res_data = DAO.execute_returning_query(UserQueries.CHECK_USER_EXIST, params)

    if len(res_data) == 0:
        print(PromptMessage.WRONG_CREDENTIALS)
        return

    print(PromptMessage.NEW_PASSWORD_PROMPT)
    new_password = validate.password_validator()
    hashed_new_password = hash_password(new_password)

    # update new password to db
    params = (hashed_new_password, user_id)
    DAO.execute_non_returning_query(UserQueries.CHANGE_PASSWORD_QUERY, params)
    logger.info("Password Changed for user %s", user_id)
    print("Password Updated Successfully")


def check_empty_data(res_data, prompt_message):
    """This function will check for whether data is there or not"""
    if len(res_data) == 0:
        logger.error(prompt_message)
        print(prompt_message)
        return True

    return False
