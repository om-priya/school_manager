import logging
from flask_smorest import abort

from handlers.user_handler import (
    view_personal_info,
    fetch_salary_history,
    change_password_handler,
)
from utils.custom_error import (
    DataNotFound,
    FailedAction,
    InvalidCredentials,
    ApplicationError,
)
from config.http_status_code import HttpStatusCode
from models.response_format import SuccessResponse, ErrorResponse
from helper.helper_function import (
    get_user_id_from_jwt,
    get_user_role_from_jwt,
    get_request_id,
)

logger = logging.getLogger(__name__)


class UserController:

    def get_my_profile(self):
        try:
            role = get_user_role_from_jwt()
            user_id = get_user_id_from_jwt()
            logger.info(f"{get_request_id()} calling handler for fetching user_profile")
            res_data = view_personal_info(role, user_id)
            logger.info(
                f"{get_request_id()} formatting response for user_profile fetched"
            )
            return SuccessResponse(200, "Your Information", res_data).get_json()
        except ApplicationError as error:
            logger.critical(f"{get_request_id()} {error.err_message}")
            return abort(
                error.code,
                message=ErrorResponse(error.code, error.err_message).get_json(),
            )

    def get_my_salary_history(self):
        try:
            user_id = get_user_id_from_jwt()

            res_data = fetch_salary_history(user_id)
            return SuccessResponse(200, "Salary History", res_data).get_json()
        except ApplicationError as error:
            logger.error(f"{get_request_id()} {error.err_message}")
            return abort(
                error.code,
                message=ErrorResponse(error.code, error.err_message).get_json(),
            )

    def change_password(self, user_details):
        try:
            role = get_user_role_from_jwt()
            user_id = get_user_id_from_jwt()

            user_name = user_details["user_name"]
            password = user_details["password"]
            new_password = user_details["new_password"]

            change_password_handler(user_id, user_name, password, new_password)

            return SuccessResponse(
                200, "Password Changed Successfully Please Log_In Again"
            ).get_json()
        except ApplicationError as error:
            logger.error(f"{get_request_id()} {error.err_message}")
            return abort(
                error.code,
                message=ErrorResponse(error.code, error.err_message).get_json(),
            )
