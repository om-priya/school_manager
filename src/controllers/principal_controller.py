""" This module is responsible for handling all the controlers for principal """
import logging
from controllers.helper.helper_function import (
    fetch_salary_history,
    view_personal_info,
)
from config.display_menu import DisplayMenu, PromptMessage
from config.sqlite_queries import PrincipalQueries
from controllers.handlers.event_handler import EventHandler
from controllers.handlers.feedback_handler import FeedbackHandler
from controllers.handlers.issue_handler import IssueHandler
from controllers.handlers.leave_handler import LeaveHandler
from controllers.handlers.teacher_handler import TeacherHandler

logger = logging.getLogger(__name__)


class PrincipalController:
    def __init__(self, user_id):
        self.user_id = user_id
        self.teacher_handler_obj = TeacherHandler()
        self.feedback_handler_obj = FeedbackHandler(self.user_id)
        self.event_handler_obj = EventHandler(self.user_id)
        self.leave_handler_obj = LeaveHandler(self.user_id)
        self.issue_handler_obj = IssueHandler(self.user_id)

    def handle_teacher(self):
        """It will handle all the teacher-related task"""
        while True:
            print(DisplayMenu.HANDLE_TEACHER_PROMPT)

            user_req = input(PromptMessage.TAKE_INPUT.format("Query [1-6]"))
            match user_req:
                case "1":
                    self.teacher_handler_obj.approve_teacher()
                case "2":
                    self.teacher_handler_obj.get_all_teacher()
                case "3":
                    self.teacher_handler_obj.get_teacher_by_id()
                case "4":
                    self.teacher_handler_obj.update_teacher()
                case "5":
                    self.teacher_handler_obj.delete_teacher()
                case "6":
                    break
                case _:
                    print(PromptMessage.INVALID_INPUT.format("Enter Only [1-6]"))

    def handle_feedbacks(self):
        """It will handle all the feedback-related task"""
        while True:
            print(DisplayMenu.FEEDBACK_PROMPT)

            user_req = input(PromptMessage.TAKE_INPUT.format("Query [1-3]"))
            match user_req:
                case "1":
                    self.feedback_handler_obj.read_feedback()
                case "2":
                    self.feedback_handler_obj.give_feedback()
                case "3":
                    break
                case _:
                    print(PromptMessage.INVALID_INPUT.format("Enter Only [1-3]"))

    def handle_events(self):
        """It will handle all the events-related task"""
        while True:
            print(DisplayMenu.EVENTS_PROMPT)

            user_req = input(PromptMessage.TAKE_INPUT.format("Query [1-2]"))
            match user_req:
                case "1":
                    self.event_handler_obj.read_event()
                case "2":
                    self.event_handler_obj.create_event()
                case "3":
                    break
                case _:
                    print(PromptMessage.INVALID_INPUT.format("Enter Only [1-3]"))

    def handle_leaves(self):
        """It will handle all the leaves-related task"""
        while True:
            print(DisplayMenu.LEAVES_PROMPT)

            user_req = input(PromptMessage.TAKE_INPUT.format("Query [1-2]"))
            match user_req:
                case "1":
                    self.leave_handler_obj.see_leave_status()
                case "2":
                    self.leave_handler_obj.apply_leave()
                case "3":
                    break
                case _:
                    print(PromptMessage.INVALID_INPUT.format("Enter Only [1-3]"))

    def view_profile(self):
        """View Profile of principal"""
        view_personal_info(PrincipalQueries.GET_PRINCIPAL_BY_ID, self.user_id)

    def view_issues(self):
        """To view the raised Issues"""
        self.issue_handler_obj.view_issue()

    def see_salary_history(self):
        """Salary History of Principal"""
        fetch_salary_history(self.user_id)
