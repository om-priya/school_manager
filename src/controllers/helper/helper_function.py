"""This file contains some helper function which are used for multiple controllers"""

import logging
from src.config.display_menu import PromptMessage
from src.config.sqlite_queries import UserQueries
from src.database.database_access import DatabaseAccess
from src.utils.pretty_print import pretty_print

logger = logging.getLogger(__name__)


def fetch_salary_history(user_id):
    """Fetching salary history of a particular user"""
    dao = DatabaseAccess()
    res_data = dao.execute_returning_query(UserQueries.GET_SALARY_HISTORY, (user_id,))

    # if there is no any records for a teacher
    if len(res_data) == 0:
        logger.error("No Salary History Found")
        print(PromptMessage.NOTHING_FOUND.format("Salary History"))
        return

    headers = ["Salary Id", "Year", "Month", "Amount", "Pay_Date"]
    pretty_print(res_data, headers)


def view_personal_info(query, user_id):
    """This function will print a user profile"""
    dao = DatabaseAccess()
    res_data = dao.execute_returning_query(query, (user_id,))

    # info for logged in user
    headers = ["Id", "Name", "phone", "email", "status"]
    pretty_print(res_data, headers)
