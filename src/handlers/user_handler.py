import logging
from config.display_menu import PromptMessage
from config.sqlite_queries import UserQueries
from database.database_access import DatabaseAccess
from utils.hash_password import hash_password
from utils.custom_error import FailedAction, DataNotFound, InvalidCredentials
from handlers.principal_handler import PrincipalHandler
from handlers.teacher_handler import TeacherHandler
from utils import validate

logger = logging.getLogger(__name__)


def fetch_salary_history(user_id):
    """Fetching salary history of a particular user"""
    res_data = DatabaseAccess.execute_returning_query(
        UserQueries.GET_SALARY_HISTORY, (user_id,)
    )

    # if there is no any records for a teacher
    if len(res_data) == 0:
        logger.error("No Salary History Found")
        raise DataNotFound

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
    params = (username, hashed_password, user_id)
    res_data = DatabaseAccess.execute_returning_query(
        UserQueries.CHECK_USER_EXIST, params
    )

    if len(res_data) == 0:
        logger.error(PromptMessage.WRONG_CREDENTIALS)
        raise InvalidCredentials

    hashed_new_password = hash_password(new_password)

    # update new password to db
    params = (hashed_new_password, user_id)
    DatabaseAccess.execute_non_returning_query(
        UserQueries.CHANGE_PASSWORD_QUERY, params
    )
    logger.info("Password Changed for user %s", user_id)
