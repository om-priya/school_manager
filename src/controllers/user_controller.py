from flask_smorest import abort

from handlers.user_handler import (
    view_personal_info,
    fetch_salary_history,
    change_password_handler,
)
from utils.custom_error import DataNotFound, FailedAction, InvalidCredentials
from models.response_format import SuccessResponse, ErrorResponse
from helper.helper_function import get_user_id_from_jwt, get_user_role_from_jwt


class UserController:
    def get_my_profile(self):
        try:
            role = get_user_role_from_jwt()
            user_id = get_user_id_from_jwt()

            res_data = view_personal_info(role, user_id)

            return SuccessResponse(200, "Your Information", res_data).get_json()
        except DataNotFound:
            return abort(
                404, message=ErrorResponse(404, "No Such User Found").get_json()
            )
        except FailedAction:
            return abort(
                403,
                message=ErrorResponse(403, "You don't have access to This").get_json(),
            )

    def get_my_salary_history(self):
        try:
            role = get_user_role_from_jwt()
            user_id = get_user_id_from_jwt()

            res_data = fetch_salary_history(user_id)
            return SuccessResponse(200, "Salary History", res_data).get_json()
        except DataNotFound:
            return abort(
                404, message=ErrorResponse(404, "No Salary History Found").get_json()
            )

    def change_password(self, user_details):
        try:
            role = get_user_role_from_jwt()
            user_id = get_user_id_from_jwt()

            user_name = user_details["user_name"]
            password = user_details["password"]
            new_password = user_details["new_password"]

            change_password_handler(user_id, user_name, password, new_password)

            # yha pe token delte karke login karne bolo
            return SuccessResponse(
                200, "Password Changed Successfully Please Log_In Again"
            ).get_json()
        except InvalidCredentials:
            abort(
                400,
                message=ErrorResponse(
                    400, "Check Your Username and Password"
                ).get_json(),
            )
