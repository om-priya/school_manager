"""Event Handler File contains code for handling event buisness logic"""

from datetime import datetime
import logging
import shortuuid

from utils.custom_error import DataNotFound
from config.sqlite_queries import CreateTable, UserQueries
from config.display_menu import PromptMessage
from database.database_access import DatabaseAccess
from helper.helper_function import check_empty_data, get_request_id

logger = logging.getLogger(__name__)


class EventHandler:
    """
    This class handles the buisness logic for reading and creating event
    """

    def __init__(self, user_id):
        self.user_id = user_id

    def read_event(self):
        """Read Events"""
        logger.info(f"{get_request_id()} Fetching Events")
        res_data = DatabaseAccess.execute_returning_query(UserQueries.READ_NOTICE)

        if check_empty_data(res_data, PromptMessage.NOTHING_FOUND.format("events")):
            logger.error(f"{get_request_id()} No such events found")
            raise DataNotFound

        logger.info(f"{get_request_id()} Returning events found")
        return res_data

    def create_event(self, notice_message):
        """Create Events"""
        notice_id = shortuuid.ShortUUID().random(length=6)
        created_by = self.user_id
        create_date = datetime.now().strftime("%d-%m-%Y")

        # Inserting into db
        logger.info(f"{get_request_id()} Started saving to events table")
        DatabaseAccess.execute_non_returning_query(
            CreateTable.INSERT_INTO_NOTICE,
            (notice_id, created_by, notice_message, create_date),
        )
        logger.info(f"{get_request_id()} saved to events table")
