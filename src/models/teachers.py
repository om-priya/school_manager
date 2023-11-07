"""This file contains a class for teacher"""
import logging
import shortuuid
from src.models.users import User
from src.config.display_menu import PromptMessage

from src.database.database_access import DatabaseAccess
from src.database.db_connector import DatabaseConnection
from src.config.sqlite_queries import TeacherQueries, CreateTable
from src.utils.exception_handler import exception_checker
from src.utils.hash_password import hash_password

logger = logging.getLogger(__name__)


class Teacher(User):
    """Teacher object which will inherit from user"""

    def __init__(self, teacher_info):
        super().__init__(
            teacher_info["name"],
            teacher_info["gender"],
            teacher_info["email"],
            teacher_info["phone"],
            teacher_info["school_name"],
        )
        self.experience = teacher_info["experience"]
        self.fav_subject = teacher_info["fav_subject"]
        self.user_id = shortuuid.ShortUUID().random(length=6)
        self.role = teacher_info["role"]
        self.password = hash_password(teacher_info["password"])
        self.status = "pending"
        self.username = teacher_info["email"].split("@")[0]

    @exception_checker
    def save_teacher(self):
        """Save Teacher To DB"""
        database_access_obj = DatabaseAccess()
        school_id = database_access_obj.execute_returning_query(
            TeacherQueries.GET_SCHOOL_ID, (self.school_name,)
        )

        if len(school_id) == 0:
            print(PromptMessage.NO_SCHOOL_FOUND)
            logger.error("No such school present in the system")
            return

        school_id = school_id[0][0]
        # creating tuple for execution
        cred_tuple = (
            self.username,
            self.password,
            self.user_id,
            self.role,
            self.status,
        )
        map_tuple = (self.user_id, school_id)
        user_tuple = (self.user_id, self.name, self.gender, self.email, self.phone)
        teacher_tuple = (self.user_id, self.experience, self.fav_subject)

        with DatabaseConnection("src\\database\\school.db") as connection:
            cursor = connection.cursor()
            cursor.execute(CreateTable.INSERT_INTO_CREDENTIAL, cred_tuple)
            cursor.execute(CreateTable.INSERT_INTO_MAPPING, map_tuple)
            cursor.execute(CreateTable.INSERT_INTO_USER, user_tuple)
            cursor.execute(TeacherQueries.INSERT_INTO_TEACHER, teacher_tuple)

        logger.info("User %s %s Saved to Db", self.name, self.role)

        logger.info("Teacher Saved to DB")
        print(PromptMessage.SIGNED_UP_SUCCESS)
