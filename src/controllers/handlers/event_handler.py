"""Event Handler File"""

from datetime import datetime
import logging
import shortuuid
from config.regex_pattern import RegexPatterns
from utils.validate import pattern_validator
from utils.pretty_print import pretty_print
from utils.custom_error import DataNotFound
from config.sqlite_queries import CreateTable, UserQueries
from config.display_menu import PromptMessage
from config.headers_for_output import TableHeaders
from database.database_access import DatabaseAccess
from controllers.helper.helper_function import check_empty_data

logger = logging.getLogger(__name__)


class EventHandler:
    def __init__(self, user_id):
        self.user_id = user_id

    def read_event(self):
        """Read Events"""
        res_data = DatabaseAccess.execute_returning_query(UserQueries.READ_NOTICE)

        if check_empty_data(res_data, PromptMessage.NOTHING_FOUND.format("Notice")):
            raise DataNotFound

        return res_data

    def create_event(self, notice_message):
        """Create Events"""
        notice_id = shortuuid.ShortUUID().random(length=6)
        created_by = self.user_id
        create_date = datetime.now().strftime("%d-%m-%Y")

        # Inserting into db
        DatabaseAccess.execute_non_returning_query(
            CreateTable.INSERT_INTO_NOTICE,
            (notice_id, created_by, notice_message, create_date),
        )
        logger.info("Added to Notice Board")
