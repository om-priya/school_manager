"""This contains teacher handler functionality"""

import logging
from config.display_menu import PromptMessage
from config.sqlite_queries import TeacherQueries
from database.database_access import DatabaseAccess

# from utils import validate
from helper.helper_function import check_empty_data, get_request_id
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
        logger.info(f"{get_request_id()} fetching status of teacher {teacher_id}")
        res_data = DatabaseAccess.execute_returning_query(
            TeacherQueries.FETCH_TEACHER_STATUS, (teacher_id,)
        )

        return res_data

    @staticmethod
    def fetch_active_teacher():
        """Fetching the id of active teacher"""
        logger.info(f"{get_request_id()} fetching all active teacher Ids")
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
            logger.error(f"{get_request_id()} No Such teacher Found")
            raise DataNotFound
        elif status[0]["status"] != "pending":
            logger.error(f"{get_request_id()} Teacher Can't be Approved")
            raise FailedAction
        else:
            # executing the query
            logger.info(f"{get_request_id()} approving teacher with id {teacher_id}")
            DatabaseAccess.execute_non_returning_query(
                TeacherQueries.APPROVE_TEACHER, (teacher_id,)
            )

    def get_all_teacher(self):
        """Get All Teachers"""
        res_data = DatabaseAccess.execute_returning_query(
            TeacherQueries.GET_ALL_TEACHER
        )

        if check_empty_data(res_data, PromptMessage.NOTHING_FOUND.format("Teachers")):
            logger.error(f"{get_request_id()} No Such teacher Found")
            raise DataNotFound

        return res_data

    def get_teacher_by_id(self, teacher_id):
        """Get Specific Teacher"""
        res_data = DatabaseAccess.execute_returning_query(
            TeacherQueries.GET_TEACHER_BY_ID, (teacher_id,)
        )

        if check_empty_data(res_data, PromptMessage.NOTHING_FOUND.format("Teachers")):
            logger.error(f"{get_request_id()} No Such teacher Found")
            raise DataNotFound

        return res_data

    def update_teacher(self, teacher_id, updated_details):
        """Update Teacher"""
        # fetching status for edge cases
        teacher_status = self.get_status(teacher_id)

        if check_empty_data(
            teacher_status, PromptMessage.NOTHING_FOUND.format("Teachers")
        ):
            raise DataNotFound

        name = updated_details["name"]
        gender = updated_details["gender"]
        email = updated_details["email"]
        phone = updated_details["phone"]
        user_table_updated = (name, gender, email, phone, teacher_id)
        # saving updates to db
        DatabaseAccess.execute_non_returning_query(
            TeacherQueries.UPDATE_TEACHER.format("user"),
            user_table_updated,
        )

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
            logger.error("Can't perform delete action on entered user_id")
            raise DataNotFound
        DatabaseAccess.execute_non_returning_query(
            TeacherQueries.DELETE_TEACHER, (teacher_id,)
        )
