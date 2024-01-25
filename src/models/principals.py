"""This file contains a class for principal"""
import logging
import shortuuid
from models.users import User
from config.display_menu import PromptMessage

from database.database_access import DatabaseAccess
from database.db_connector import DatabaseConnection
from config.sqlite_queries import (
    PrincipalQueries,
    TeacherQueries,
    CreateTable,
    DatabaseConfig,
)
from utils.exception_handler import exception_checker
from utils.hash_password import hash_password

logger = logging.getLogger(__name__)


class Principal(User):
    """
    Principal class inherits from User for storing principal-specific information.

    Attributes:
    - experience (str): The experience of the principal.
    - user_id (str): The unique identifier for the principal.
    - role (str): The role of the principal.
    - password (str): The hashed password of the principal.
    - status (str): The status of the principal.
    - username (str): The username derived from the principal's email.
    """

    def __init__(self, principal_info):
        """
        Initializes a Principal object with principal-specific information.

        Parameters:
        - principal_info (dict): A dictionary containing principal information.
        """
        super().__init__(
            principal_info["name"],
            principal_info["gender"],
            principal_info["email"],
            principal_info["phone"],
            principal_info["school_name"],
        )
        self.experience = principal_info["experience"]
        self.role = "principal"
        self.username = principal_info["email"].split("@")[0]
        self.user_id = shortuuid.ShortUUID().random(length=6)
        self.status = "pending"
        self.password = hash_password(principal_info["password"])

    def save_principal(self):
        """
        Save the Principal object to the database.

        Raises:
        - ValueError: If school is not found or principal_info is invalid.

        Returns:
        None
        """
        school_id = DatabaseAccess.execute_returning_query(
            TeacherQueries.GET_SCHOOL_ID, (self.school_name,)
        )
        if len(school_id) == 0:
            print(PromptMessage.NO_SCHOOL_FOUND)
            return

        school_id = school_id[0]["school_id"]
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
        principal_tuple = (self.user_id, self.experience)

        with DatabaseConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(CreateTable.INSERT_INTO_CREDENTIAL, cred_tuple)
            cursor.execute(CreateTable.INSERT_INTO_MAPPING, map_tuple)
            cursor.execute(CreateTable.INSERT_INTO_USER, user_tuple)
            cursor.execute(PrincipalQueries.INSERT_INTO_PRINCIPAL, principal_tuple)

        logger.info("User %s %s Saved to Db", self.name, self.role)

        logger.info("Principal Saved to DB")
        print(PromptMessage.SIGNED_UP_SUCCESS)
