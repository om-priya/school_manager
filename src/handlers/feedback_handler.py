"""Feed Back Handler File"""

from datetime import datetime
import logging
import shortuuid
from config.sqlite_queries import TeacherQueries, CreateTable, PrincipalQueries
from config.display_menu import PromptMessage
from database.database_access import DatabaseAccess
from helper.helper_function import check_empty_data
from utils.custom_error import DataNotFound

logger = logging.getLogger(__name__)


class FeedbackHandler:
    def __init__(self, user_id):
        self.user_id = user_id

    def read_feedback(self):
        """Read Feedbacks"""
        res_data = DatabaseAccess.execute_returning_query(
            PrincipalQueries.READ_FEEDBACKS_PRINCIPAL, (self.user_id,)
        )

        if check_empty_data(res_data, PromptMessage.NOTHING_FOUND.format("FeedBack")):
            raise DataNotFound

        return res_data

    def give_feedback(self, teacher_id, f_message):
        """Create Feedbacks"""
        res_data = DatabaseAccess.execute_returning_query(
            TeacherQueries.GET_APPROVED_TEACHER
        )

        if check_empty_data(res_data, PromptMessage.NOTHING_FOUND.format("Teacher")):
            raise DataNotFound

        # checking teacher's Id
        for data in res_data:
            if data[0] == teacher_id:
                break
        else:
            logger.error("Wrong Teacher Id")
            raise DataNotFound

        # Taking Info and saving it to db
        f_id = shortuuid.ShortUUID().random(length=6)
        created_date = datetime.now().strftime("%d-%m-%Y")

        DatabaseAccess.execute_non_returning_query(
            CreateTable.INSERT_INTO_FEEDBACKS,
            (f_id, f_message, created_date, teacher_id, self.user_id),
        )
        logger.info("Feedback Created")
