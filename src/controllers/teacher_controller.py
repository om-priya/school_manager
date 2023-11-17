""" This Module Contains all the functionality that a teacher can perform """
import logging
from src.controllers.handlers.event_handler import read_event
from src.controllers.helper.helper_function import (
    fetch_salary_history,
    view_personal_info,
    check_empty_data,
)
from src.config.display_menu import PromptMessage
from src.config.headers_for_output import TableHeaders
from src.config.sqlite_queries import TeacherQueries, UserQueries
from src.controllers.handlers import issue_handler as IssueHandler
from src.database import database_access as DAO
from src.utils.pretty_print import pretty_print

logger = logging.getLogger(__name__)


def view_profile(user_id):
    """To view personal data for a teacher"""
    view_personal_info(TeacherQueries.GET_TEACHER_BY_ID, user_id)


def read_notice():
    """To view notice board of a school"""
    read_event()


def read_feedbacks(user_id):
    """To view feedbacks from teacher"""
    res_data = DAO.execute_returning_query(UserQueries.READ_FEEDBACKS, (user_id,))

    # if there is no feedbacks for a teacher
    if check_empty_data(res_data, PromptMessage.NOTHING_FOUND.format("Feedback")):
        return

    headers = (
        TableHeaders.ID.format("Feedback"),
        TableHeaders.MESSAGE.format("Feedbacks"),
        TableHeaders.CREATED_DATE,
    )
    pretty_print(res_data, headers=headers)


def raise_issue(user_id):
    """Raise Issue"""
    IssueHandler.raise_issue(user_id)


def salary_history(user_id):
    """To view salary history for a teacher"""
    fetch_salary_history(user_id)
