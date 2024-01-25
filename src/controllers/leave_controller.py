from flask_jwt_extended import get_jwt
from flask_smorest import abort

from handlers.leave_handler import LeaveHandler
from models.response_format import SuccessResponse, ErrorResponse
from utils.custom_error import DataNotFound


class LeavesController:
    def get_leave_info(self):
        try:
            jwt = get_jwt()
            user_id = jwt.get("sub").get("user_id")

            res_data = LeaveHandler(user_id).see_leave_status()
            return SuccessResponse(200, "List of Leaves", res_data).get_json()
        except DataNotFound:
            return abort(404, message=ErrorResponse(404, "No Leave Records Found").get_json())

    def apply_for_leave(self, leave_details):
        jwt = get_jwt()
        user_id = jwt.get("sub").get("user_id")

        LeaveHandler(user_id).apply_leave(
            leave_details["leave_date"], leave_details["no_of_daya"]
        )
        return SuccessResponse(200, "Leave Applied SuccessFully").get_json()

    def approve_leave(self, leave_info):
        try:
            LeaveHandler.approve_leave(leave_info["leave_id"])
            return SuccessResponse(200, "Leave Approved Successfully").get_json()
        except DataNotFound:
            return abort(404, message=ErrorResponse(404, "No Leave Records Found").get_json())
