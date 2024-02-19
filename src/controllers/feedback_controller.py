import logging
from handlers.feedback_handler import FeedbackHandler
from flask_smorest import abort
from models.response_format import SuccessResponse, ErrorResponse
from config.display_menu import PromptMessage
from utils.custom_error import DataNotFound
from helper.helper_function import (
    get_user_id_from_jwt,
    get_request_id,
    get_user_role_from_jwt,
)

logger = logging.getLogger(__name__)


class FeedbackController:
    def get_all_feedbacks(self):
        try:
            user_id = get_user_id_from_jwt()
            role = get_user_role_from_jwt()
            logger.info(f"{get_request_id()} calling handler for reading feedbacks")
            res_data = FeedbackHandler(user_id).read_feedback(role)

            logger.info(f"{get_request_id()} Feedbacks found now formatting response")
            return SuccessResponse(
                200, PromptMessage.LIST_ENTRY.format("Feedbacks"), res_data
            ).get_json()
        except DataNotFound:
            logger.error(
                f"{get_request_id()} Feedbacks not found now formatting response"
            )
            return abort(
                404,
                message=ErrorResponse(
                    404, PromptMessage.NOTHING_FOUND.format("Feedback")
                ).get_json(),
            )

    def give_teacher_feedback(self, teacher_id, feedback_info):
        try:
            user_id = get_user_id_from_jwt()
            logger.info(
                f"{get_request_id()} calling the handler for giving feedback to {teacher_id}"
            )
            FeedbackHandler(user_id).give_feedback(
                teacher_id, feedback_info["feedback_message"]
            )
            logger.info(
                f"{get_request_id()} Feedbacks created for teacher {teacher_id}"
            )
            return SuccessResponse(
                201, PromptMessage.ADDED_SUCCESSFULLY.format("Feedback")
            ).get_json()
        except DataNotFound:
            logger.error(f"{get_request_id()} Wrong Teacher Id Provided")
            return abort(
                404,
                message=ErrorResponse(
                    404, PromptMessage.NOTHING_FOUND.format("Teacher")
                ).get_json(),
            )
