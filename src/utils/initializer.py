"""This Function will run before main and create table and db"""

import logging
from src.database.database_access import DatabaseAccess
from src.database.db_connector import DatabaseConnection
from src.config.sqlite_queries import CreateTable, UserQueries
from src.super_admin_info import create_super_admin

logger = logging.getLogger(__name__)


def initialize_app():
    """Create Db and super admin"""

    # creating table in the db
    with DatabaseConnection("src\\database\\school.db") as connection:
        cursor = connection.cursor()
        # query to create table only once
        cursor.execute(CreateTable.CREATE_CREDENTIALS_TABLE)
        cursor.execute(CreateTable.CREATE_USERS_TABLE)
        cursor.execute(CreateTable.CREATE_USER_SCHOOL_MAP_TABLE)
        cursor.execute(CreateTable.CREATE_SCHOOL_TABLE)
        cursor.execute(CreateTable.CREATE_LEAVE_TABLE)
        cursor.execute(CreateTable.CREATE_NOTICE_TABLE)
        cursor.execute(CreateTable.CREATE_ISSUES_TABLE)
        cursor.execute(CreateTable.CREATE_FEEDBACKS_TABLE)
        cursor.execute(CreateTable.CREATE_PRINCIPAL_TABLE)
        cursor.execute(CreateTable.CREATE_TEACHER_TABLE)
        cursor.execute(CreateTable.CREATE_STAFF_MEMBER_TABLE)
        cursor.execute(CreateTable.CREATE_SALARY_TABLE)
        logger.debug("Table Created only once")

    # checking if super admin exists or not
    dao = DatabaseAccess()

    res_data = dao.execute_returning_query(UserQueries.FETCH_SUPER_ADMIN)

    # super admin exists in table
    if len(res_data) != 0:
        return

    # create super admin
    create_super_admin()
