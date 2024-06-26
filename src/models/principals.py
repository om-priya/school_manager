"""This file contains a class for principal"""

import logging
import shortuuid
from models.users import User

from database.database_access import DatabaseAccess
from database.db_connector import DatabaseConnection
from config.sqlite_queries import (
    PrincipalQueries,
    TeacherQueries,
    CreateTable,
)
from config.http_status_code import HttpStatusCode
from config.display_menu import PromptMessage
from helper.helper_function import get_request_id
from utils.hash_password import hash_password
from utils.custom_error import ApplicationError

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


class SavePrincipal:
    """
    Save Principal class to initiate the process of saving to db
    """

    def save_principal(self, principla_obj):
        """
        Save the Principal object to the database.

        Raises:
        - ValueError: If school is not found or principal_info is invalid.

        Returns:
        None
        """
        school_id = DatabaseAccess.execute_returning_query(
            TeacherQueries.GET_SCHOOL_ID, (principla_obj.school_name,)
        )
        if len(school_id) == 0:
            logger.error(f"{get_request_id()} no such school present in the system")
            raise ApplicationError(
                HttpStatusCode.NOT_FOUND, PromptMessage.NOTHING_FOUND.format("School")
            )

        school_id = school_id[0]["school_id"]
        # creating tuple for execution
        cred_tuple = (
            principla_obj.username,
            principla_obj.password,
            principla_obj.user_id,
            principla_obj.role,
            principla_obj.status,
        )
        map_tuple = (principla_obj.user_id, school_id)
        user_tuple = (
            principla_obj.user_id,
            principla_obj.name,
            principla_obj.gender,
            principla_obj.email,
            principla_obj.phone,
        )
        principal_tuple = (principla_obj.user_id, principla_obj.experience)

        with DatabaseConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(CreateTable.INSERT_INTO_CREDENTIAL, cred_tuple)
            cursor.execute(CreateTable.INSERT_INTO_MAPPING, map_tuple)
            cursor.execute(CreateTable.INSERT_INTO_USER, user_tuple)
            cursor.execute(PrincipalQueries.INSERT_INTO_PRINCIPAL, principal_tuple)

        logger.info(f"{get_request_id()} User %s %s Saved to Db", principla_obj.name, principla_obj.role)
