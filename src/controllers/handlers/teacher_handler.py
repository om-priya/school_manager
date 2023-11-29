"""This contains teacher handler functionality"""
import logging
from config.regex_pattern import RegexPatterns
from config.headers_for_output import TableHeaders
from config.display_menu import PromptMessage
from config.sqlite_queries import TeacherQueries
from database.database_access import DatabaseAccess
from utils.pretty_print import pretty_print
from utils.exception_handler import exception_checker
from utils import validate
from controllers.helper.helper_function import check_empty_data

logger = logging.getLogger(__name__)


class TeacherHandler:
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

    @exception_checker
    def approve_teacher(self):
        """Approve Teacher"""
        teacher_id = validate.uuid_validator(
            PromptMessage.APPROVE_PROMPT.format("Teacher's Id"),
            RegexPatterns.UUID_PATTERN,
        )

        # fetching status of teacher with teacher_id
        status = self.get_status(teacher_id)

        # checks to handle edge cases
        if check_empty_data(status, PromptMessage.NOTHING_FOUND.format("Teachers")):
            return
        elif status[0][0] != "pending":
            logger.error("Teacher Can't be Approved")
            print(PromptMessage.APPROVE_FAILED.format("Teacher"))
            return
        else:
            # executing the query
            DatabaseAccess.execute_non_returning_query(
                TeacherQueries.APPROVE_TEACHER, (teacher_id,)
            )

        print(PromptMessage.ADDED_SUCCESSFULLY.format("Teacher"))

    @exception_checker
    def get_all_teacher(self):
        """Get All Teachers"""
        res_data = DatabaseAccess.execute_returning_query(
            TeacherQueries.GET_ALL_TEACHER
        )

        if check_empty_data(res_data, PromptMessage.NOTHING_FOUND.format("Teachers")):
            return

        headers = (
            TableHeaders.ID.format("User"),
            TableHeaders.NAME,
            TableHeaders.PHONE,
            TableHeaders.EMAIL,
            TableHeaders.STATUS,
        )
        pretty_print(res_data, headers)

    @exception_checker
    def get_teacher_by_id(self):
        """Get Specific Teacher"""
        teacher_id = validate.uuid_validator(
            PromptMessage.TAKE_SPECIFIC_ID.format("Teacher"), RegexPatterns.UUID_PATTERN
        )

        res_data = DatabaseAccess.execute_returning_query(
            TeacherQueries.GET_TEACHER_BY_ID, (teacher_id,)
        )

        if check_empty_data(res_data, PromptMessage.NOTHING_FOUND.format("Teachers")):
            return

        headers = (
            TableHeaders.ID.format("User"),
            TableHeaders.NAME,
            TableHeaders.PHONE,
            TableHeaders.EMAIL,
            TableHeaders.STATUS,
        )
        pretty_print(res_data, headers)

    @exception_checker
    def update_teacher(self):
        """Update Teacher"""
        teacher_id = validate.uuid_validator(
            PromptMessage.TAKE_SPECIFIC_ID.format("Teacher"), RegexPatterns.UUID_PATTERN
        )
        field_to_update = input(PromptMessage.FIELD_UPDATE)
        options = ("name", "phone", "email", "experience")
        options = (
            TableHeaders.NAME.lower(),
            TableHeaders.PHONE.lower(),
            TableHeaders.EMAIL.lower(),
            TableHeaders.EXPERIENCE.lower(),
        )

        # checking whether entered field is correct or not
        if field_to_update not in options:
            logger.info("Wrong Field Name")
            print(PromptMessage.NOTHING_FOUND.format("For Field Name"))
            return

        # fetching status for edge cases
        teacher_status = self.get_status(teacher_id)

        if check_empty_data(
            teacher_status, PromptMessage.NOTHING_FOUND.format("Teachers")
        ):
            return

        if teacher_status[0][0] != "active":
            logger.info("Can't perform update action on entered user_id")
            print(PromptMessage.FAILED_ACTION.format("Update"))
            return

        # getting table name and validating updated value
        if field_to_update in options[:3]:
            table_name = "user"
            if field_to_update == "name":
                updated_value = validate.pattern_validator(
                    PromptMessage.TAKE_INPUT.format("Name"), RegexPatterns.NAME_PATTERN
                )
            elif field_to_update == "phone":
                updated_value = validate.pattern_validator(
                    PromptMessage.TAKE_INPUT.format("Phone Number"),
                    RegexPatterns.PHONE_PATTERN,
                )
            else:
                updated_value = validate.pattern_validator(
                    PromptMessage.TAKE_INPUT.format("email"),
                    RegexPatterns.EMAIL_PATTERN,
                )
        else:
            table_name = "teacher"
            updated_value = validate.pattern_validator(
                PromptMessage.TAKE_INPUT.format("Experience in Year"),
                RegexPatterns.EXPERIENCE_PATTERN,
            )

        # saving updates to db
        DatabaseAccess.execute_non_returning_query(
            TeacherQueries.UPDATE_TEACHER.format(table_name, field_to_update),
            (updated_value, teacher_id),
        )

        print(PromptMessage.SUCCESS_ACTION.format("Updated"))

    @exception_checker
    def delete_teacher(self):
        """Delete Teacher of principal"""
        teacher_id = validate.uuid_validator(
            PromptMessage.TAKE_SPECIFIC_ID.format("Teacher"), RegexPatterns.UUID_PATTERN
        )

        active_teachers_id = self.fetch_active_teacher()

        if check_empty_data(
            active_teachers_id, PromptMessage.NOTHING_FOUND.format("Teachers")
        ):
            return

        for tid in active_teachers_id:
            if tid[0] == teacher_id:
                break
        else:
            print(PromptMessage.FAILED_ACTION.format("Delete"))
            return
        DatabaseAccess.execute_non_returning_query(
            TeacherQueries.DELETE_TEACHER, (teacher_id,)
        )
