""" This project aims to provide a management system for a school 
through which they can manage different entities in their school. 
The base assumption of this project is that it manages with the perspective of one school 
To check for super admin credentials go to /src/super_admin_meny.py """
import logging
from config.display_menu import DisplayMenu, PromptMessage
from menu import UserScreen
from controllers.user_controller import AuthenticationController
from utils.initializer import initialize_app

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
    level=logging.DEBUG,
    filename="logs.log",
)

logger = logging.getLogger(__name__)


def main():
    """This Function is responsible for making my app run contineously"""

    # setting initial value to default
    is_logged_in = False
    user_id = ""
    role = ""

    while True:
        # For login and signup
        while not is_logged_in:
            print(DisplayMenu.ENTRY_POINT_PROMPT)

            user_req = input(PromptMessage.TAKE_INPUT.format("Query"))
            if user_req == "1":
                # Function returning 3 things
                is_logged_in, user_id, role = AuthenticationController.is_logged_in()
            elif user_req == "2":
                # saving to db with status pending
                AuthenticationController.sign_up()
            else:
                print(PromptMessage.INVALID_INPUT.format("Only [1,2]"))

        logger.info("Logged in user: %s, role: %s", user_id, role)

        user_screen = UserScreen(user_id)
        while True:
            if role == "superadmin":
                user_screen.super_admin_menu()
            elif role == "principal":
                user_screen.principal_menu()
            elif role == "teacher":
                user_screen.teacher_menu()
            else:
                print(PromptMessage.DENIED_ACCESS.format("to access Portal"))
            # Resetting the variable due to logged out functionality
            is_logged_in = False
            user_id = ""
            role = ""
            break


if __name__ == "__main__":
    # created db with all the tables and run main function
    initialize_app()
    main()
