""" This Module Contains all the functionality that a teacher can perform """
import logging
from src.controllers.handlers.event_handler import read_event
from src.controllers.helper.helper_function import (
    fetch_salary_history,
    view_personal_info,
)
from src.config.display_menu import PromptMessage
from src.config.sqlite_queries import TeacherQueries, UserQueries
from src.controllers.handlers import issue_handler as IssueHandler
from src.database.database_access import DatabaseAccess
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
    dao = DatabaseAccess()
    res_data = dao.execute_returning_query(UserQueries.READ_FEEDBACKS, (user_id,))

    # if there is no feedbacks for a teacher
    if len(res_data) == 0:
        logger.error("Nothing on Feedbacks for You")
        print(PromptMessage.NOTHING_FOUND.format("Feedback"))
        return

    headers = ["ID", "Message", "Created Date"]
    pretty_print(res_data, headers=headers)


def raise_issue(user_id):
    """Raise Issue"""
    IssueHandler.raise_issue(user_id)


def salary_history(user_id):
    """To view salary history for a teacher"""
    fetch_salary_history(user_id)
