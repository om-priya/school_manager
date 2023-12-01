""" This Module Contains all the functionality that a teacher can perform """
import logging
from controllers.handlers.event_handler import EventHandler
from controllers.helper.helper_function import (
    fetch_salary_history,
    view_personal_info,
    check_empty_data,
)
from config.display_menu import PromptMessage, DisplayMenu
from config.headers_for_output import TableHeaders
from config.sqlite_queries import TeacherQueries, UserQueries
from controllers.handlers.issue_handler import IssueHandler
from controllers.handlers.leave_handler import LeaveHandler
from database.database_access import DatabaseAccess
from utils.pretty_print import pretty_print

logger = logging.getLogger(__name__)


class TeacherController:
    def __init__(self, user_id):
        self.user_id = user_id
        self.event_handler_obj = EventHandler(self.user_id)
        self.leave_handler_obj = LeaveHandler(self.user_id)
        self.issue_handler_obj = IssueHandler(self.user_id)

    def view_profile(self):
        """To view personal data for a teacher"""
        view_personal_info(TeacherQueries.GET_TEACHER_BY_ID, self.user_id)

    def read_notice(self):
        """To view notice board of a school"""
        self.event_handler_obj.read_event()

    def read_feedbacks(self):
        """To view feedbacks from teacher"""
        res_data = DatabaseAccess.execute_returning_query(
            UserQueries.READ_FEEDBACKS, (self.user_id,)
        )

        # if there is no feedbacks for a teacher
        if check_empty_data(res_data, PromptMessage.NOTHING_FOUND.format("Feedback")):
            return

        headers = (
            TableHeaders.ID.format("Feedback"),
            TableHeaders.MESSAGE.format("Feedbacks"),
            TableHeaders.CREATED_DATE,
        )
        pretty_print(res_data, headers=headers)

    def raise_issue(self):
        """Raise Issue"""
        self.issue_handler_obj.raise_issue()

    def salary_history(self):
        """To view salary history for a teacher"""
        fetch_salary_history(self.user_id)

    def handle_leaves(self):
        """It will handle all the leaves related functionality"""
        while True:
            print(DisplayMenu.LEAVES_PROMPT)

            user_req = input(PromptMessage.TAKE_INPUT.format("Query [1-3]"))
            match user_req:
                case "1":
                    self.leave_handler_obj.see_leave_status()
                case "2":
                    self.leave_handler_obj.apply_leave()
                case "3":
                    break
                case _:
                    print(PromptMessage.INVALID_INPUT.format("Enter Only [1-3]"))
