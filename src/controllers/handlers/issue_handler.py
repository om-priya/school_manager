"""This file contains Issue Handler Class"""

import logging
import shortuuid
from src.config.regex_pattern import RegexPatterns
from src.config.sqlite_queries import UserQueries, CreateTable
from src.config.display_menu import PromptMessage
from src.config.headers_for_output import TableHeaders
from src.database import database_access as DAO
from src.utils.pretty_print import pretty_print
from src.utils.validate import pattern_validator
from src.controllers.helper.helper_function import check_empty_data

logger = logging.getLogger(__name__)


def view_issue():
    """Showing all the Raised Issues"""
    res_data = DAO.execute_returning_query(UserQueries.GET_ALL_ISSUES)

    if check_empty_data(res_data, PromptMessage.NOTHING_FOUND.format("Issues")):
        return

    headers = (
        TableHeaders.ID.format("Issue"),
        TableHeaders.MESSAGE.format("Issue"),
        TableHeaders.RAISED_BY,
    )
    pretty_print(res_data, headers)


def raise_issue(user_id):
    """To raise issue for the management"""
    issue_id = shortuuid.ShortUUID().random(length=6)
    issue_mssg = pattern_validator(
        PromptMessage.TAKE_INPUT.format("Issue Message"), RegexPatterns.MESSAGE_PATTERN
    )

    DAO.execute_non_returning_query(
        CreateTable.INSERT_INTO_ISSUE, (issue_id, issue_mssg, user_id)
    )

    logger.info("Issue Created Successfully")
    print(PromptMessage.ADDED_SUCCESSFULLY.format("Issue"))
