"""Leave Handler File"""

import logging
from datetime import datetime
import shortuuid
from src.config.regex_pattern import RegexPatterns
from src.config.sqlite_queries import UserQueries, CreateTable
from src.config.display_menu import PromptMessage
from src.config.headers_for_output import TableHeaders
from src.database import database_access as DAO
from src.utils.pretty_print import pretty_print
from src.utils.validate import pattern_validator

logger = logging.getLogger(__name__)


def apply_leave(user_id):
    """Apply Leave"""
    leave_id = shortuuid.ShortUUID().random(length=6)
    leave_date = pattern_validator(PromptMessage.DATE_INPUT, RegexPatterns.DATE_PATTERN)

    curr_date = datetime.now().strftime("%d-%m-%Y")

    if leave_date <= curr_date:
        logger.error("%s leave_date is previous to curr date %s", leave_date, curr_date)
        print(PromptMessage.INVALID_DATE.format(leave_date, curr_date))
        return

    no_of_days = pattern_validator(
        PromptMessage.TAKE_INPUT.format("No of Days for leave"),
        RegexPatterns.DAYS_PATTERN,
    )

    DAO.execute_non_returning_query(
        CreateTable.INSERT_INTO_LEAVES,
        (leave_id, leave_date, no_of_days, user_id, "pending"),
    )

    logger.info("Applied to leave by user %s", user_id)
    print(PromptMessage.ADDED_SUCCESSFULLY.format("Leave Request"))


def see_leave_status(user_id):
    """See Leave Status"""
    res_data = DAO.execute_returning_query(UserQueries.FETCH_LEAVE_STATUS, (user_id,))

    if len(res_data) == 0:
        logger.error("No Leaves Record Found for user %s", user_id)
        print(PromptMessage.NOTHING_FOUND.format("Leaves Record"))
        return

    headers = (TableHeaders.LEAVE_DATE, TableHeaders.NO_OF_DAYS, TableHeaders.STATUS)

    pretty_print(res_data, headers=headers)
