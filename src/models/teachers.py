"""This file contains a class for teacher"""

import logging
import shortuuid
from models.users import User
from database.database_access import DatabaseAccess
from database.db_connector import DatabaseConnection
from config.sqlite_queries import TeacherQueries, CreateTable
from config.display_menu import PromptMessage
from utils.hash_password import hash_password
from utils.custom_error import DataNotFound
from helper.helper_function import get_request_id

logger = logging.getLogger(__name__)


class Teacher(User):
    """
    Teacher class inherits from User for storing teacher-specific information.

    Attributes:
    - experience (str): The experience of the teacher.
    - fav_subject (str): The favorite subject of the teacher.
    - user_id (str): The unique identifier for the teacher.
    - role (str): The role of the teacher.
    - password (str): The hashed password of the teacher.
    - status (str): The status of the teacher.
    - username (str): The username derived from the teacher's email.
    """

    def __init__(self, teacher_info):
        """
        Initializes a Teacher object with teacher-specific information.

        Parameters:
        - teacher_info (dict): A dictionary containing teacher information.
        """
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


class SaveTeacher:
    """
    Save Teacher class to initiate the process of saving to db
    """

    def save_teacher(self, teacher_obj):
        """
        Save the Teacher object to the database.

        Raises:
        - ValueError: If school is not found or teacher_info is invalid.

        Returns:
        None
        """
        school_id = DatabaseAccess.execute_returning_query(
            TeacherQueries.GET_SCHOOL_ID, (teacher_obj.school_name,)
        )
        if len(school_id) == 0:
            logger.error(f"{get_request_id()} No such school present in the system")
            raise DataNotFound

        school_id = school_id[0]["school_id"]
        # creating tuple for execution
        cred_tuple = (
            teacher_obj.username,
            teacher_obj.password,
            teacher_obj.user_id,
            teacher_obj.role,
            teacher_obj.status,
        )
        map_tuple = (teacher_obj.user_id, school_id)
        user_tuple = (
            teacher_obj.user_id,
            teacher_obj.name,
            teacher_obj.gender,
            teacher_obj.email,
            teacher_obj.phone,
        )
        teacher_tuple = (
            teacher_obj.user_id,
            teacher_obj.experience,
            teacher_obj.fav_subject,
        )

        with DatabaseConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(CreateTable.INSERT_INTO_CREDENTIAL, cred_tuple)
            cursor.execute(CreateTable.INSERT_INTO_MAPPING, map_tuple)
            cursor.execute(CreateTable.INSERT_INTO_USER, user_tuple)
            cursor.execute(TeacherQueries.INSERT_INTO_TEACHER, teacher_tuple)

        logger.info(
            f"{get_request_id()} User %s %s Saved to Db",
            teacher_obj.name,
            teacher_obj.role,
        )
