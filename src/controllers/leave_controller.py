from flask_smorest import abort
from handlers.leave_handler import LeaveHandler
from models.response_format import SuccessResponse, ErrorResponse
from utils.custom_error import DataNotFound
from helper.helper_function import get_user_id_from_jwt

class LeavesController:
    def get_leave_info(self):
        try:
            user_id = get_user_id_from_jwt()

            res_data = LeaveHandler(user_id).see_leave_status()
            return SuccessResponse(200, "List of Leaves", res_data).get_json()
        except DataNotFound:
            return abort(404, message=ErrorResponse(404, "No Leave Records Found").get_json())

    def apply_for_leave(self, leave_details):
        user_id = get_user_id_from_jwt()

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
