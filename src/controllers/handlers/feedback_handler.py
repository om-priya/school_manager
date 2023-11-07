"""Feed Back Handler File"""

from datetime import datetime
import logging
import shortuuid
from src.config.regex_pattern import RegexPatterns
from src.utils.pretty_print import pretty_print
from src.utils.validate import pattern_validator
from src.config.sqlite_queries import TeacherQueries, CreateTable, PrincipalQueries
from src.config.display_menu import PromptMessage
from src.database.database_access import DatabaseAccess

logger = logging.getLogger(__name__)


def read_feedback(user_id):
    """Read Feedbacks"""
    print("\nHere's the feedback given by you\n")

    dao = DatabaseAccess()
    res_data = dao.execute_returning_query(
        PrincipalQueries.READ_FEEDBACKS_PRINCIPAL, (user_id,)
    )

    if len(res_data) == 0:
        logger.error("No Feedbacks Found by user %s", user_id)
        print(PromptMessage.NOTHING_FOUND.format("FeedBack"))
        return

    headers = ["ID", "Message", "Created Date"]
    pretty_print(res_data, headers)


def give_feedback(user_id):
    """Create Feedbacks"""
    dao = DatabaseAccess()
    res_data = dao.execute_returning_query(TeacherQueries.GET_APPROVED_TEACHER)

    if len(res_data) == 0:
        logger.error("No Teacher Present in the system")
        print(PromptMessage.NOTHING_FOUND.format("Teacher"))
        return

    print("Select User ID from the available teachers list")
    headers = ["ID", "Name"]
    pretty_print(res_data, headers=headers)

    teacher_id = pattern_validator(
        PromptMessage.TAKE_SPECIFIC_ID.format("Teacher's"), RegexPatterns.UUID_PATTERN
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

    dao.execute_non_returning_query(
        CreateTable.INSERT_INTO_FEEDBACKS,
        (f_id, f_message, created_date, teacher_id, user_id),
    )
    logger.info("Feedback Created")
    print(PromptMessage.ADDED_SUCCESSFULLY.format("Feedbacks"))
