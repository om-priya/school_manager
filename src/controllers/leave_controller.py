import logging
from flask_smorest import abort
from handlers.leave_handler import LeaveHandler
from models.response_format import SuccessResponse, ErrorResponse
from utils.custom_error import DataNotFound
from helper.helper_function import get_user_id_from_jwt, get_request_id, get_user_role_from_jwt
from config.display_menu import PromptMessage

logger = logging.getLogger(__name__)


class LeavesController:
    def get_leave_info(self):
        try:
            user_id = get_user_id_from_jwt()
            role = get_user_role_from_jwt()
            logger.info(
                f"{get_request_id()} calling handler for fetching leave records"
            )
            res_data = LeaveHandler(user_id).see_leave_status(role)
            logger.info(
                f"{get_request_id()} formatting response for leave records fetched"
            )
            return SuccessResponse(
                200, PromptMessage.LIST_ENTRY.format("Leaves Record"), res_data
            ).get_json()
        except DataNotFound:
            logger.error(
                f"{get_request_id()} formatting response for no leave record found"
            )
            return abort(
                404,
                message=ErrorResponse(
                    404, PromptMessage.NOTHING_FOUND.format("Leave Record")
                ).get_json(),
            )

    def apply_for_leave(self, leave_details):
        user_id = get_user_id_from_jwt()
        logger.info(f"{get_request_id()} calling handler for creating leave request")
        LeaveHandler(user_id).apply_leave(
            leave_details["leave_date"], leave_details["no_of_days"]
        )
        logger.info(f"{get_request_id()} Leave Request created successfully formating response")
        return SuccessResponse(
            201, PromptMessage.ADDED_SUCCESSFULLY.format("Leave Request")
        ).get_json(), 201

    def approve_leave(self, leave_info):
        try:
            logger.info(f"{get_request_id()} calling handler for approving leave request")

            LeaveHandler.approve_leave(leave_info["leave_id"])

            logger.info(f"{get_request_id()} Leave Request approved successfully formating response")
            return SuccessResponse(
                200, PromptMessage.APPROVE_SUCCESS.format("Leave")
            ).get_json()
        except DataNotFound:
            logger.error(f"{get_request_id()} formatting response for no leave record found for leave_id {leave_info['leave_id']}")
            return abort(
                404,
                message=ErrorResponse(
                    404, PromptMessage.NOTHING_FOUND.format("Leave Record")
                ).get_json(),
            )
