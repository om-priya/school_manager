"""This file contains a class for principal"""
import logging
import shortuuid
from src.models.users import User
from src.config.display_menu import PromptMessage

from src.database.database_access import DatabaseAccess
from src.database.db_connector import DatabaseConnection
from src.config.sqlite_queries import PrincipalQueries, TeacherQueries, CreateTable
from src.utils.exception_handler import exception_checker
from src.utils.hash_password import hash_password

logger = logging.getLogger(__name__)


class Principal(User):
    """Principal Class which will inherit from User"""

    def __init__(self, principal_info):
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

    @exception_checker
    def save_principal(self):
        """Save Principal to DB"""
        database_access_obj = DatabaseAccess()
        school_id = database_access_obj.execute_returning_query(
            TeacherQueries.GET_SCHOOL_ID, (self.school_name,)
        )
        if len(school_id) == 0:
            print(PromptMessage.NO_SCHOOL_FOUND)
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
        principal_tuple = (self.user_id, self.experience)

        with DatabaseConnection("src\\database\\school.db") as connection:
            cursor = connection.cursor()
            cursor.execute(CreateTable.INSERT_INTO_CREDENTIAL, cred_tuple)
            cursor.execute(CreateTable.INSERT_INTO_MAPPING, map_tuple)
            cursor.execute(CreateTable.INSERT_INTO_USER, user_tuple)
            cursor.execute(PrincipalQueries.INSERT_INTO_PRINCIPAL, principal_tuple)

        logger.info("User %s %s Saved to Db", self.name, self.role)

        logger.info("Principal Saved to DB")
        print(PromptMessage.NO_SCHOOL_FOUND)
