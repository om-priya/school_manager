"""Event Handler File"""

from datetime import datetime
import logging
import shortuuid
from src.config.regex_pattern import RegexPatterns
from src.utils.validate import pattern_validator
from src.utils.pretty_print import pretty_print
from src.config.sqlite_queries import CreateTable, UserQueries
from src.config.display_menu import PromptMessage
from src.database.database_access import DatabaseAccess

logger = logging.getLogger(__name__)


def read_event():
    """Read Events"""
    dao = DatabaseAccess()
    res_data = dao.execute_returning_query(UserQueries.READ_NOTICE)

    if len(res_data) == 0:
        logger.error("No Records On Notice Board")
        print(PromptMessage.NOTHING_FOUND.format("Notice"))
        return

    headers = ["ID", "Message"]
    pretty_print(res_data, headers)


def create_event(user_id):
    """Create Events"""
    dao = DatabaseAccess()

    notice_id = shortuuid.ShortUUID().random(length=6)
    created_by = user_id
    notice_mssg = pattern_validator(
        PromptMessage.TAKE_INPUT.format("Notice Message"), RegexPatterns.MESSAGE_PATTERN
    )
    create_date = datetime.now().strftime("%d-%m-%Y")

    # Inserting into db
    dao.execute_non_returning_query(
        CreateTable.INSERT_INTO_NOTICE,
        (notice_id, created_by, notice_mssg, create_date),
    )
    logger.info("Added to Notice Board")
    print(PromptMessage.ADDED_SUCCESSFULLY.format("Notice"))
