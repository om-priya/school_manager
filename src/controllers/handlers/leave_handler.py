"""Leave Handler File"""

import logging
from datetime import datetime
import shortuuid
from config.regex_pattern import RegexPatterns
from config.sqlite_queries import UserQueries, CreateTable
from config.display_menu import PromptMessage
from config.headers_for_output import TableHeaders
from database.database_access import DatabaseAccess
from utils.pretty_print import pretty_print
from utils.validate import pattern_validator, validate_date
from utils.exception_handler import exception_checker
from controllers.helper.helper_function import check_empty_data

logger = logging.getLogger(__name__)


class LeaveHandler:
    def __init__(self, user_id):
        self.user_id = user_id

    @exception_checker
    def apply_leave(self):
        """Apply Leave"""
        leave_id = shortuuid.ShortUUID().random(length=6)

        # to handle date which fits the format but can't be possible in real world
        leave_date = validate_date(PromptMessage.DATE_INPUT)

        no_of_days = pattern_validator(
            PromptMessage.TAKE_INPUT.format("No of Days for leave"),
            RegexPatterns.DAYS_PATTERN,
        )

        DatabaseAccess.execute_non_returning_query(
            CreateTable.INSERT_INTO_LEAVES,
            (leave_id, leave_date, no_of_days, self.user_id, "pending"),
        )

        logger.info("Applied to leave by user %s", self.user_id)
        print(PromptMessage.ADDED_SUCCESSFULLY.format("Leave Request"))

    @exception_checker
    def see_leave_status(self):
        """See Leave Status"""
        res_data = DatabaseAccess.execute_returning_query(
            UserQueries.FETCH_LEAVE_STATUS, (self.user_id,)
        )

        if check_empty_data(
            res_data, PromptMessage.NOTHING_FOUND.format("Leaves Record")
        ):
            return

        headers = (
            TableHeaders.LEAVE_DATE,
            TableHeaders.NO_OF_DAYS,
            TableHeaders.STATUS,
        )

        pretty_print(res_data, headers=headers)
