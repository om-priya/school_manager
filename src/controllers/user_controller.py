from flask_jwt_extended import get_jwt
from flask_smorest import abort

from handlers.user_handler import (
    view_personal_info,
    fetch_salary_history,
    change_password_handler,
)
from utils.custom_error import DataNotFound, FailedAction, InvalidCredentials
from models.response_format import SuccessResponse, ErrorResponse


class UserController:
    def get_my_profile(self):
        try:
            jwt = get_jwt()
            role = jwt.get("sub").get("role")
            user_id = jwt.get("sub").get("user_id")

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
            jwt = get_jwt()
            role = jwt.get("sub").get("role")
            user_id = jwt.get("sub").get("user_id")

            res_data = fetch_salary_history(user_id)
            return SuccessResponse(200, "Salary History", res_data).get_json()
        except DataNotFound:
            return abort(
                404, message=ErrorResponse(404, "No Salary History Found").get_json()
            )

    def change_password(self, user_details):
        try:
            jwt = get_jwt()
            role = jwt.get("sub").get("role")
            user_id = jwt.get("sub").get("user_id")

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
