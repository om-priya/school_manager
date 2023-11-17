"""This File COntains the Menu of Different roles through Which a end-point user can 
go through different modules"""
from src.config.display_menu import DisplayMenu, PromptMessage
from src.controllers import principal_controller as PrincipalController
from src.controllers import super_admin_controller as SuperAdminController
from src.controllers import teacher_controller as TeacherController
from src.controllers.helper.helper_function import change_password
from src.utils.exception_handler import exception_checker


@exception_checker
def super_admin_menu(user_id):
    """Contains Menu For Super Admin"""
    print(DisplayMenu.SUPER_ADMIN_MAIN_PROMPT)

    user_req = input(PromptMessage.TAKE_INPUT.format("Query [1-6]"))

    while True:
        match user_req:
            case "1":
                SuperAdminController.handle_principal()
            case "2":
                SuperAdminController.handle_staff(user_id=user_id)
            case "3":
                SuperAdminController.distribute_salary()
            case "4":
                SuperAdminController.approve_leave()
            case "5":
                change_password(user_id)
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
def principal_menu(user_id):
    """Contains Menu For Principal"""
    print(DisplayMenu.PRINCIPAL_MAIN_PROMPT)

    user_req = input(PromptMessage.TAKE_INPUT.format("Query [1-9]"))

    while True:
        match user_req:
            case "1":
                PrincipalController.handle_teacher()
            case "2":
                PrincipalController.handle_feedbacks(user_id=user_id)
            case "3":
                PrincipalController.handle_events(user_id=user_id)
            case "4":
                PrincipalController.handle_leaves(user_id=user_id)
            case "5":
                PrincipalController.view_profile(user_id=user_id)
            case "6":
                PrincipalController.see_salary_history(user_id=user_id)
            case "7":
                PrincipalController.view_issues()
            case "8":
                change_password(user_id)
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
def teacher_menu(user_id):
    """Contains Menu For Teacher"""
    print(DisplayMenu.TEACHER_MAIN_PROMPT)

    user_req = input(PromptMessage.TAKE_INPUT.format("Query [1-7]"))

    while True:
        match user_req:
            case "1":
                TeacherController.view_profile(user_id=user_id)
            case "2":
                TeacherController.read_notice()
            case "3":
                TeacherController.read_feedbacks(user_id=user_id)
            case "4":
                TeacherController.raise_issue(user_id=user_id)
            case "5":
                TeacherController.salary_history(user_id=user_id)
            case "6":
                change_password(user_id)
            case "7":
                print(PromptMessage.LOGGED_OUT)
            case _:
                print(PromptMessage.INVALID_INPUT.format("Enter only [1-7]"))
        # breaking from super admin loop
        if user_req in ["6", "7"]:
            break

        print(DisplayMenu.TEACHER_MAIN_PROMPT)
        user_req = input(PromptMessage.TAKE_INPUT.format("Query [1-7]"))
