"""Event Handler File"""

from datetime import datetime
import logging
import shortuuid
from src.config.regex_pattern import RegexPatterns
from src.utils.validate import pattern_validator
from src.utils.pretty_print import pretty_print
from src.utils.exception_handler import exception_checker
from src.config.sqlite_queries import CreateTable, UserQueries
from src.config.display_menu import PromptMessage
from src.config.headers_for_output import TableHeaders
from src.database import database_access as DAO
from src.controllers.helper.helper_function import check_empty_data

logger = logging.getLogger(__name__)


@exception_checker
def read_event():
    """Read Events"""
    res_data = DAO.execute_returning_query(UserQueries.READ_NOTICE)

    if check_empty_data(res_data, PromptMessage.NOTHING_FOUND.format("Notice")):
        return

    headers = (TableHeaders.ID.format("Notice"), TableHeaders.MESSAGE.format("Notice"))
    pretty_print(res_data, headers)


@exception_checker
def create_event(user_id):
    """Create Events"""
    notice_id = shortuuid.ShortUUID().random(length=6)
    created_by = user_id
    notice_mssg = pattern_validator(
        PromptMessage.TAKE_INPUT.format("Notice Message"), RegexPatterns.MESSAGE_PATTERN
    )
    create_date = datetime.now().strftime("%d-%m-%Y")

    # Inserting into db
    DAO.execute_non_returning_query(
        CreateTable.INSERT_INTO_NOTICE,
        (notice_id, created_by, notice_mssg, create_date),
    )
    logger.info("Added to Notice Board")
    print(PromptMessage.ADDED_SUCCESSFULLY.format("Notice"))
