"""This file contains Issue Handler Class"""

import logging
import shortuuid
from config.regex_pattern import RegexPatterns
from config.sqlite_queries import UserQueries, CreateTable
from config.display_menu import PromptMessage
from config.headers_for_output import TableHeaders
from database.database_access import DatabaseAccess
from utils.pretty_print import pretty_print
from utils.validate import pattern_validator
from utils.exception_handler import exception_checker
from controllers.helper.helper_function import check_empty_data

logger = logging.getLogger(__name__)


class IssueHandler:
    def __init__(self, user_id):
        self.user_id = user_id

    @exception_checker
    def view_issue(self):
        """Showing all the Raised Issues"""
        res_data = DatabaseAccess.execute_returning_query(UserQueries.GET_ALL_ISSUES)

        if check_empty_data(res_data, PromptMessage.NOTHING_FOUND.format("Issues")):
            return

        headers = (
            TableHeaders.ID.format("Issue"),
            TableHeaders.MESSAGE.format("Issue"),
            TableHeaders.RAISED_BY,
        )
        pretty_print(res_data, headers)

    @exception_checker
    def raise_issue(self):
        """To raise issue for the management"""
        issue_id = shortuuid.ShortUUID().random(length=6)
        issue_mssg = pattern_validator(
            PromptMessage.TAKE_INPUT.format("Issue Message"),
            RegexPatterns.MESSAGE_PATTERN,
        )

        DatabaseAccess.execute_non_returning_query(
            CreateTable.INSERT_INTO_ISSUE, (issue_id, issue_mssg, self.user_id)
        )

        logger.info("Issue Created Successfully")
        print(PromptMessage.ADDED_SUCCESSFULLY.format("Issue"))
