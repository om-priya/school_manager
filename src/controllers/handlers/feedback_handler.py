"""Feed Back Handler File"""

from datetime import datetime
import logging
import shortuuid
from config.regex_pattern import RegexPatterns
from config.headers_for_output import TableHeaders
from utils.pretty_print import pretty_print
from utils.validate import pattern_validator, uuid_validator
from utils.exception_handler import exception_checker
from config.sqlite_queries import TeacherQueries, CreateTable, PrincipalQueries
from config.display_menu import PromptMessage
from database.database_access import DatabaseAccess
from controllers.helper.helper_function import check_empty_data

logger = logging.getLogger(__name__)


class FeedbackHandler:
    def __init__(self, user_id):
        self.user_id = user_id

    @exception_checker
    def read_feedback(self):
        """Read Feedbacks"""
        res_data = DatabaseAccess.execute_returning_query(
            PrincipalQueries.READ_FEEDBACKS_PRINCIPAL, (self.user_id,)
        )

        if check_empty_data(res_data, PromptMessage.NOTHING_FOUND.format("FeedBack")):
            return

        headers = (
            TableHeaders.ID.format("Feedback"),
            TableHeaders.MESSAGE.format("Feedback"),
            TableHeaders.CREATED_DATE,
        )
        pretty_print(res_data, headers)

    @exception_checker
    def give_feedback(self):
        """Create Feedbacks"""
        res_data = DatabaseAccess.execute_returning_query(
            TeacherQueries.GET_APPROVED_TEACHER
        )

        if check_empty_data(res_data, PromptMessage.NOTHING_FOUND.format("Teacher")):
            return

        print("Select User ID from the available teachers list")
        headers = (TableHeaders.ID.format("Teacher"), TableHeaders.NAME)
        pretty_print(res_data, headers=headers)

        teacher_id = uuid_validator(
            PromptMessage.TAKE_SPECIFIC_ID.format("Teacher's"),
            RegexPatterns.UUID_PATTERN,
        )

        # checking teacher's Id
        for data in res_data:
            if data[0] == teacher_id:
                break
        else:
            logger.error("Wrong Teacher Id")
            print(PromptMessage.NOTHING_FOUND.format("Teacher"))
            return

        # Taking Info and saving it to db
        f_id = shortuuid.ShortUUID().random(length=6)
        f_message = pattern_validator(
            PromptMessage.TAKE_INPUT.format("Message"), RegexPatterns.MESSAGE_PATTERN
        )
        created_date = datetime.now().strftime("%d-%m-%Y")

        DatabaseAccess.execute_non_returning_query(
            CreateTable.INSERT_INTO_FEEDBACKS,
            (f_id, f_message, created_date, teacher_id, self.user_id),
        )
        logger.info("Feedback Created")
        print(PromptMessage.ADDED_SUCCESSFULLY.format("Feedbacks"))
