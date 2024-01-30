"""This contains teacher handler functionality"""
import logging
from config.display_menu import PromptMessage
from config.sqlite_queries import TeacherQueries
from database.database_access import DatabaseAccess

# from utils import validate
from helper.helper_function import check_empty_data
from utils.custom_error import DataNotFound, FailedAction

logger = logging.getLogger(__name__)


class TeacherHandler:
    """
    This class handles the buisness logic for handling
    CRUD on Teacher
    """

    @staticmethod
    def get_status(teacher_id):
        """This Function Will be responsible for fetching status"""
        res_data = DatabaseAccess.execute_returning_query(
            TeacherQueries.FETCH_TEACHER_STATUS, (teacher_id,)
        )

        return res_data

    @staticmethod
    def fetch_active_teacher():
        """Fetching the id of active teacher"""
        res_data = DatabaseAccess.execute_returning_query(
            TeacherQueries.FETCH_ACTIVE_TEACHER_ID
        )

        return res_data

    def approve_teacher(self, teacher_id):
        """Approve Teacher"""
        # fetching status of teacher with teacher_id
        status = self.get_status(teacher_id)

        # checks to handle edge cases
        if check_empty_data(status, PromptMessage.NOTHING_FOUND.format("Teachers")):
            raise DataNotFound
        elif status[0]["status"] != "pending":
            logger.error("Teacher Can't be Approved")
            raise FailedAction
        else:
            # executing the query
            DatabaseAccess.execute_non_returning_query(
                TeacherQueries.APPROVE_TEACHER, (teacher_id,)
            )

    def get_all_teacher(self):
        """Get All Teachers"""
        res_data = DatabaseAccess.execute_returning_query(
            TeacherQueries.GET_ALL_TEACHER
        )

        if check_empty_data(res_data, PromptMessage.NOTHING_FOUND.format("Teachers")):
            raise DataNotFound

        return res_data

    def get_teacher_by_id(self, teacher_id):
        """Get Specific Teacher"""
        res_data = DatabaseAccess.execute_returning_query(
            TeacherQueries.GET_TEACHER_BY_ID, (teacher_id,)
        )

        if check_empty_data(res_data, PromptMessage.NOTHING_FOUND.format("Teachers")):
            raise DataNotFound

        return res_data

    # def update_teacher(self):
    #     """Update Teacher"""
    #     teacher_id = validate.uuid_validator(
    #         PromptMessage.TAKE_SPECIFIC_ID.format("Teacher"), RegexPatterns.UUID_PATTERN
    #     )
    #     field_to_update = input(PromptMessage.FIELD_UPDATE)
    #     options = (
    #         TableHeaders.NAME.lower(),
    #         TableHeaders.PHONE.lower(),
    #         TableHeaders.EMAIL.lower(),
    #         TableHeaders.EXPERIENCE.lower(),
    #     )

    #     # checking whether entered field is correct or not
    #     if field_to_update not in options:
    #         logger.info("Wrong Field Name")
    #         print(PromptMessage.NOTHING_FOUND.format("For Field Name"))
    #         return

    #     # fetching status for edge cases
    #     teacher_status = self.get_status(teacher_id)

    #     if check_empty_data(
    #         teacher_status, PromptMessage.NOTHING_FOUND.format("Teachers")
    #     ):
    #         return

    #     if teacher_status[0][0] != "active":
    #         logger.info("Can't perform update action on entered user_id")
    #         print(PromptMessage.FAILED_ACTION.format("Update"))
    #         return

    #     # getting table name and validating updated value
    #     if field_to_update in options[:3]:
    #         table_name = "user"
    #         if field_to_update == "name":
    #             updated_value = validate.pattern_validator(
    #                 PromptMessage.TAKE_INPUT.format("Name"), RegexPatterns.NAME_PATTERN
    #             )
    #         elif field_to_update == "phone":
    #             updated_value = validate.pattern_validator(
    #                 PromptMessage.TAKE_INPUT.format("Phone Number"),
    #                 RegexPatterns.PHONE_PATTERN,
    #             )
    #         else:
    #             updated_value = validate.pattern_validator(
    #                 PromptMessage.TAKE_INPUT.format("email"),
    #                 RegexPatterns.EMAIL_PATTERN,
    #             )
    #     else:
    #         table_name = "teacher"
    #         updated_value = validate.pattern_validator(
    #             PromptMessage.TAKE_INPUT.format("Experience in Year"),
    #             RegexPatterns.EXPERIENCE_PATTERN,
    #         )

    #     # saving updates to db
    #     DatabaseAccess.execute_non_returning_query(
    #         TeacherQueries.UPDATE_TEACHER.format(table_name, field_to_update),
    #         (updated_value, teacher_id),
    #     )

    #     print(PromptMessage.SUCCESS_ACTION.format("Updated"))

    def delete_teacher(self, teacher_id):
        """Delete Teacher of principal"""
        active_teachers_id = self.fetch_active_teacher()

        if check_empty_data(
            active_teachers_id, PromptMessage.NOTHING_FOUND.format("Teachers")
        ):
            raise DataNotFound

        for tid in active_teachers_id:
            if tid["user_id"] == teacher_id:
                break
        else:
            logger.error("Can\'t perform delete action on entered user_id")
            raise DataNotFound
        DatabaseAccess.execute_non_returning_query(
            TeacherQueries.DELETE_TEACHER, (teacher_id,)
        )
