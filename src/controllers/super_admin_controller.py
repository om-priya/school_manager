""" This Module is Responsible for handling super admin functionality """

import logging
from datetime import datetime
import shortuuid
from src.config.display_menu import DisplayMenu, PromptMessage
from src.config.regex_pattern import RegexPatterns
from src.config.sqlite_queries import (
    TeacherQueries,
    PrincipalQueries,
    UserQueries,
    CreateTable,
)
from src.controllers.handlers import principal_handler as PrincipalHandler
from src.controllers.handlers import staff_handler as StaffHandler
from src.database.database_access import DatabaseAccess
from src.utils.pretty_print import pretty_print
from src.utils import validate

logger = logging.getLogger(__name__)


def handle_principal():
    """Handling Principal"""
    print(DisplayMenu.HANDLE_PRINCIPAL_PROMPT)

    user_req = input(PromptMessage.TAKE_INPUT.format("Query [1-5]"))
    match user_req:
        case "1":
            PrincipalHandler.approve_principal()
        case "2":
            PrincipalHandler.get_all_principal()
        case "3":
            PrincipalHandler.get_principal_by_id()
        case "4":
            PrincipalHandler.update_principal()
        case "5":
            PrincipalHandler.delete_principal()
        case _:
            print(PromptMessage.INVALID_INPUT)


def handle_staff(user_id):
    """Handling Staff"""
    print(DisplayMenu.HANDLE_STAFF_PROMPT)

    user_req = input(PromptMessage.TAKE_INPUT.format("Query [1-4]"))
    match user_req:
        case "1":
            StaffHandler.view_staff(user_id=user_id)
        case "2":
            StaffHandler.create_staff(user_id=user_id)
        case "3":
            StaffHandler.update_staff()
        case "4":
            StaffHandler.delete_staff()
        case _:
            print(PromptMessage.INVALID_INPUT)


def distribute_salary():
    """Distribute Salary"""
    TEACHER_SALARY = 1000
    PRINCIPAL_SALARY = 5000
    # Getting values to insert it in db
    year = datetime.now().year
    month = datetime.now().strftime("%m")
    pay_date = datetime.now().strftime("%d-%m-%Y")

    # fetching active teacher id
    dao = DatabaseAccess()
    res_data = dao.execute_returning_query(TeacherQueries.FETCH_ACTIVE_TEACHER_ID)

    # Inserting into salary db
    if len(res_data) == 0:
        print(PromptMessage.NOTHING_FOUND.format("Teacher"))
    else:
        print("Initiating Teacher Salary")
        for teacher_id in res_data[0]:
            salary_id = shortuuid.ShortUUID().random(length=6)
            salary_tuple = (
                salary_id,
                teacher_id,
                TEACHER_SALARY,
                year,
                month,
                pay_date,
            )
            dao.execute_non_returning_query(
                CreateTable.INSERT_INTO_SALARY, salary_tuple
            )

    # fetching active principal id
    res_data = dao.execute_returning_query(PrincipalQueries.FETCH_PRINCIPAL_ID)

    # Inserting into db
    if len(res_data) == 0:
        print(PromptMessage.NOTHING_FOUND.format("Principal"))
    else:
        print("Initiating Principal Salary")
        for principal_id in res_data[0]:
            salary_id = shortuuid.ShortUUID().random(length=6)
            salary_tuple = (
                salary_id,
                principal_id,
                PRINCIPAL_SALARY,
                year,
                month,
                pay_date,
            )
            dao.execute_non_returning_query(
                CreateTable.INSERT_INTO_SALARY, salary_tuple
            )


def approve_leave():
    """Approve Leave"""
    dao = DatabaseAccess()
    res_data = dao.execute_returning_query(UserQueries.GET_PENDING_LEAVES)

    # if there are no leave request
    if len(res_data) == 0:
        logger.info("No Pending Leave Request")
        print(PromptMessage.NOTHING_FOUND.format("Pending leave request"))
        return

    headers = ["Leave_Id", "Starting Date", "No_of_Days", "User_id", "Status"]
    pretty_print(res_data, headers)

    # will happen nothing if Id was not right
    leave_id = validate.pattern_validator(
        PromptMessage.APPROVE_PROMPT.format("leave id"), RegexPatterns.UUID_PATTERN
    )

    dao.execute_non_returning_query(UserQueries.APPROVE_LEAVE, (leave_id,))
