"""This file contains Issue Handler Class"""

import logging
import shortuuid
from src.config.regex_pattern import RegexPatterns
from src.config.sqlite_queries import UserQueries, CreateTable
from src.config.display_menu import PromptMessage
from src.database.database_access import DatabaseAccess
from src.utils.pretty_print import pretty_print
from src.utils.validate import pattern_validator

logger = logging.getLogger(__name__)


def view_issue():
    """Showing all the Raised Issues"""
    dao = DatabaseAccess()
    res_data = dao.execute_returning_query(UserQueries.GET_ALL_ISSUES)

    if len(res_data) == 0:
        logger.error("No issues Found")
        print(PromptMessage.NOTHING_FOUND.format("Issues"))
        return

    headers = ["issue_id", "issue_text", "raised_by"]
    pretty_print(res_data, headers)


def raise_issue(user_id):
    """To raise issue for the management"""
    issue_id = shortuuid.ShortUUID().random(length=6)
    issue_mssg = pattern_validator(
        PromptMessage.TAKE_INPUT.format("Issue Message"), RegexPatterns.MESSAGE_PATTERN
    )

    dao = DatabaseAccess()
    dao.execute_non_returning_query(
        CreateTable.INSERT_INTO_ISSUE, (issue_id, issue_mssg, user_id)
    )

    logger.info("Issue Created Successfully")
    print(PromptMessage.ADDED_SUCCESSFULLY.format("Issue"))
