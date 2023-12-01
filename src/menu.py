"""This File COntains the Menu of Different roles through Which a end-point user can 
go through different modules"""
from config.display_menu import DisplayMenu, PromptMessage
from controllers.principal_controller import PrincipalController
from controllers.super_admin_controller import SuperAdminController
from controllers.teacher_controller import TeacherController
from controllers.helper.helper_function import change_password
from utils.exception_handler import exception_checker


class UserScreen:
    def __init__(self, user_id):
        self.user_id = user_id

    @exception_checker
    def super_admin_menu(self):
        """Contains Menu For Super Admin"""
        print(DisplayMenu.SUPER_ADMIN_MAIN_PROMPT)

        user_req = input(PromptMessage.TAKE_INPUT.format("Query [1-6]"))

        super_admin_controller_obj = SuperAdminController(self.user_id)
        while True:
            match user_req:
                case "1":
                    super_admin_controller_obj.handle_principal()
                case "2":
                    super_admin_controller_obj.handle_staff()
                case "3":
                    super_admin_controller_obj.distribute_salary()
                case "4":
                    super_admin_controller_obj.approve_leave()
                case "5":
                    change_password(self.user_id)
                case "6":
                    print(PromptMessage.LOGGED_OUT)
                case _:
                    print(PromptMessage.INVALID_INPUT.format("Enter only [1-6]"))
            # breaking from super admin loop
            if user_req in ["5", "6"]:
                break

            print(DisplayMenu.SUPER_ADMIN_MAIN_PROMPT)
            user_req = input(PromptMessage.TAKE_INPUT.format("Query [1-6]"))

    @exception_checker
    def principal_menu(self):
        """Contains Menu For Principal"""
        print(DisplayMenu.PRINCIPAL_MAIN_PROMPT)

        user_req = input(PromptMessage.TAKE_INPUT.format("Query [1-9]"))

        principal_controller_obj = PrincipalController(self.user_id)
        while True:
            match user_req:
                case "1":
                    principal_controller_obj.handle_teacher()
                case "2":
                    principal_controller_obj.handle_feedbacks()
                case "3":
                    principal_controller_obj.handle_events()
                case "4":
                    principal_controller_obj.handle_leaves()
                case "5":
                    principal_controller_obj.view_profile()
                case "6":
                    principal_controller_obj.see_salary_history()
                case "7":
                    principal_controller_obj.view_issues()
                case "8":
                    change_password(self.user_id)
                case "9":
                    print(PromptMessage.LOGGED_OUT)
                case _:
                    print(PromptMessage.INVALID_INPUT.format("Enter only [1-9]"))
            # breaking from super admin loop
            if user_req in ["8", "9"]:
                break

            print(DisplayMenu.PRINCIPAL_MAIN_PROMPT)
            user_req = input(PromptMessage.TAKE_INPUT.format("Query [1-9]"))

    @exception_checker
    def teacher_menu(self):
        """Contains Menu For Teacher"""
        print(DisplayMenu.TEACHER_MAIN_PROMPT)

        user_req = input(PromptMessage.TAKE_INPUT.format("Query [1-8]"))

        teacher_controller_obj = TeacherController(self.user_id)

        while True:
            match user_req:
                case "1":
                    teacher_controller_obj.view_profile()
                case "2":
                    teacher_controller_obj.read_notice()
                case "3":
                    teacher_controller_obj.read_feedbacks()
                case "4":
                    teacher_controller_obj.raise_issue()
                case "5":
                    teacher_controller_obj.salary_history()
                case "6":
                    teacher_controller_obj.handle_leaves()
                case "7":
                    change_password(self.user_id)
                case "8":
                    print(PromptMessage.LOGGED_OUT)
                case _:
                    print(PromptMessage.INVALID_INPUT.format("Enter only [1-8]"))
            # breaking from super admin loop
            if user_req in ["7", "8"]:
                break

            print(DisplayMenu.TEACHER_MAIN_PROMPT)
            user_req = input(PromptMessage.TAKE_INPUT.format("Query [1-8]"))
