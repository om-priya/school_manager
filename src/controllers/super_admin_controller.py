""" This Module is Responsible for handling super admin functionality """
import logging
from datetime import datetime
import shortuuid
from config.display_menu import DisplayMenu, PromptMessage
from config.regex_pattern import RegexPatterns
from config.headers_for_output import TableHeaders
from config.sqlite_queries import (
    TeacherQueries,
    PrincipalQueries,
    UserQueries,
    CreateTable,
)
from handlers.principal_handler import PrincipalHandler
from handlers.staff_handler import StaffHandler
from helper.helper_function import check_empty_data
from database.database_access import DatabaseAccess
from utils.pretty_print import pretty_print
from utils import validate

logger = logging.getLogger(__name__)


class SuperAdminController:
    def __init__(self, user_id):
        """
        Initializes a SuperAdminController object.

        Parameters:
        - user_id (str): The unique identifier for the super admin.
        """
        self.user_id = user_id
        self.principal_handler_obj = PrincipalHandler()
        self.staff_handler_obj = StaffHandler(self.user_id)

    def handle_principal(self):
        """Handle principal-related tasks."""
        while True:
            print(DisplayMenu.HANDLE_PRINCIPAL_PROMPT)

            user_req = input(PromptMessage.TAKE_INPUT.format("Query [1-6]"))
            match user_req:
                case "1":
                    self.principal_handler_obj.approve_principal()
                case "2":
                    self.principal_handler_obj.get_all_principal()
                case "3":
                    self.principal_handler_obj.get_principal_by_id()
                case "4":
                    self.principal_handler_obj.update_principal()
                case "5":
                    self.principal_handler_obj.delete_principal()
                case "6":
                    break
                case _:
                    print(PromptMessage.INVALID_INPUT.format("Enter Only [1-6]"))

    def handle_staff(self):
        """Handle staff-related tasks."""
        while True:
            print(DisplayMenu.HANDLE_STAFF_PROMPT)

            user_req = input(PromptMessage.TAKE_INPUT.format("Query [1-5]"))
            match user_req:
                case "1":
                    self.staff_handler_obj.view_staff()
                case "2":
                    self.staff_handler_obj.create_staff()
                case "3":
                    self.staff_handler_obj.update_staff()
                case "4":
                    self.staff_handler_obj.delete_staff()
                case "5":
                    break
                case _:
                    print(PromptMessage.INVALID_INPUT.format("Enter Only [1-5]"))

    def distribute_salary(self):
        """Distribute salary to teachers and principals."""
        TEACHER_SALARY = 1000
        PRINCIPAL_SALARY = 5000
        # Getting values to insert it in db
        year = datetime.now().year
        month = datetime.now().strftime("%m")
        pay_date = datetime.now().strftime("%d-%m-%Y")

        # fetching active teacher id
        res_data = DatabaseAccess.execute_returning_query(
            TeacherQueries.FETCH_ACTIVE_TEACHER_ID
        )

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
                DatabaseAccess.execute_non_returning_query(
                    CreateTable.INSERT_INTO_SALARY, salary_tuple
                )

        # fetching active principal id
        res_data = DatabaseAccess.execute_returning_query(
            PrincipalQueries.FETCH_PRINCIPAL_ID
        )

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
                DatabaseAccess.execute_non_returning_query(
                    CreateTable.INSERT_INTO_SALARY, salary_tuple
                )

    def approve_leave(self):
        """Approve Pending Leaves of teacher and principal"""
        res_data = DatabaseAccess.execute_returning_query(
            UserQueries.GET_PENDING_LEAVES
        )

        # if there are no leave request
        if check_empty_data(
            res_data, PromptMessage.NOTHING_FOUND.format("Pending leave request")
        ):
            return

        headers = (
            TableHeaders.ID.format("Leave"),
            TableHeaders.STARTING_DATE,
            TableHeaders.NO_OF_DAYS,
            TableHeaders.ID.format("User"),
            TableHeaders.STATUS,
        )
        pretty_print(res_data, headers)

        # will happen nothing if Id was not right
        leave_id = validate.uuid_validator(
            PromptMessage.APPROVE_PROMPT.format("leave id"), RegexPatterns.UUID_PATTERN
        )

        # checking for valid id
        for leave_record in res_data:
            if leave_id == leave_record[0]:
                break
        else:
            print(PromptMessage.NOTHING_FOUND.format("Leave Record"))
            return

        DatabaseAccess.execute_non_returning_query(
            UserQueries.APPROVE_LEAVE, (leave_id,)
        )
        print(PromptMessage.ADDED_SUCCESSFULLY.format("Leave"))
