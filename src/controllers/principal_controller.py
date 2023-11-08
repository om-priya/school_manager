""" This module is responsible for handling all the controlers for principal """

import logging
from src.controllers.helper.helper_function import (
    fetch_salary_history,
    view_personal_info,
)
from src.config.display_menu import DisplayMenu, PromptMessage
from src.config.sqlite_queries import PrincipalQueries
from src.controllers.handlers import event_handler as EventHandler
from src.controllers.handlers import feedback_handler as FeedBackHandler
from src.controllers.handlers import issue_handler as IssueHandler
from src.controllers.handlers import leave_handler as LeaveHandler
from src.controllers.handlers import teacher_handler as TeacherHandler

logger = logging.getLogger(__name__)


def handle_teacher():
    """It will handle all the teacher related functionality"""
    print(DisplayMenu.HANDLE_TEACHER_PROMPT)

    user_req = input(PromptMessage.TAKE_INPUT.format("Query [1-5]"))
    match user_req:
        case "1":
            TeacherHandler.approve_teacher()
        case "2":
            TeacherHandler.get_all_teacher()
        case "3":
            TeacherHandler.get_teacher_by_id()
        case "4":
            TeacherHandler.update_teacher()
        case "5":
            TeacherHandler.delete_teacher()
        case _:
            print(PromptMessage.INVALID_INPUT)


def handle_feedbacks(user_id):
    """It will handle all the feedback related functionality"""
    print(DisplayMenu.FEEDBACK_PROMPT)

    user_req = input(PromptMessage.TAKE_INPUT.format("Query [1-2]"))
    match user_req:
        case "1":
            FeedBackHandler.read_feedback(user_id=user_id)
        case "2":
            FeedBackHandler.give_feedback(user_id=user_id)
        case _:
            print(PromptMessage.INVALID_INPUT)


def handle_events(user_id):
    """It will handle all the events related functionality"""
    print(DisplayMenu.EVENTS_PROMPT)

    user_req = input(PromptMessage.TAKE_INPUT.format("Query [1-2]"))
    match user_req:
        case "1":
            EventHandler.read_event()
        case "2":
            EventHandler.create_event(user_id=user_id)
        case _:
            print(PromptMessage.INVALID_INPUT)


def handle_leaves(user_id):
    """It will handle all the leaves related functionality"""
    print(DisplayMenu.LEAVES_PROMPT)

    user_req = input(PromptMessage.TAKE_INPUT.format("Query [1-2]"))
    match user_req:
        case "1":
            LeaveHandler.see_leave_status(user_id=user_id)
        case "2":
            LeaveHandler.apply_leave(user_id=user_id)
        case _:
            print(PromptMessage.INVALID_INPUT)


def view_profile(user_id):
    """View Profile of principal"""
    view_personal_info(PrincipalQueries.GET_PRINCIPAL_BY_ID, user_id)


def view_issues():
    """To view the raised Issues"""
    IssueHandler.view_issue()


def see_salary_history(user_id):
    """Salary History of Principal"""
    fetch_salary_history(user_id)
