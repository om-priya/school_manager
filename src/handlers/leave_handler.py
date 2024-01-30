"""Leave Handler File"""

import logging
import shortuuid
from config.sqlite_queries import UserQueries, CreateTable
from config.display_menu import PromptMessage
from database.database_access import DatabaseAccess
from helper.helper_function import check_empty_data
from utils.custom_error import DataNotFound

logger = logging.getLogger(__name__)


class LeaveHandler:
    """
    This class handles the buisness logic for checking leave status
    and applying for leave
    """

    def __init__(self, user_id):
        self.user_id = user_id

    def apply_leave(self, leave_date, no_of_days):
        """Apply Leave"""
        leave_id = shortuuid.ShortUUID().random(length=6)

        DatabaseAccess.execute_non_returning_query(
            CreateTable.INSERT_INTO_LEAVES,
            (leave_id, leave_date, no_of_days, self.user_id, "pending"),
        )

        logger.info("Applied to leave by user %s", self.user_id)

    def see_leave_status(self):
        """See Leave Status"""
        res_data = DatabaseAccess.execute_returning_query(
            UserQueries.FETCH_LEAVE_STATUS, (self.user_id,)
        )

        if check_empty_data(
            res_data, PromptMessage.NOTHING_FOUND.format("Leaves Record")
        ):
            raise DataNotFound

        return res_data

    @staticmethod
    def approve_leave(leave_id):
        """Approve Pending Leaves of teacher and principal"""
        res_data = DatabaseAccess.execute_returning_query(
            UserQueries.GET_PENDING_LEAVES
        )

        # if there are no leave request
        if check_empty_data(
            res_data, PromptMessage.NOTHING_FOUND.format("Pending leave request")
        ):
            raise DataNotFound

        # checking for valid id
        for leave_record in res_data:
            if leave_id == leave_record["leave_id"]:
                break
        else:
            logger.error("No such leave record Found")
            raise DataNotFound

        DatabaseAccess.execute_non_returning_query(
            UserQueries.APPROVE_LEAVE, (leave_id,)
        )
        logger.info("Leave Applied Successfully")
