import logging
from handlers.feedback_handler import FeedbackHandler
from flask_smorest import abort
from models.response_format import SuccessResponse, ErrorResponse
from config.display_menu import PromptMessage
from config.http_status_code import HttpStatusCode
from utils.custom_error import ApplicationError
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
                HttpStatusCode.SUCCESS,
                PromptMessage.LIST_ENTRY.format("Feedbacks"),
                res_data,
            ).get_json()
        except ApplicationError as error:
            logger.error(f"{get_request_id()} {error.err_message}")
            return abort(
                error.code,
                message=ErrorResponse(error.code, error.err_message).get_json(),
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
                HttpStatusCode.SUCCESS_CREATED,
                PromptMessage.ADDED_SUCCESSFULLY.format("Feedback"),
            ).get_json()
        except ApplicationError as error:
            logger.error(f"{get_request_id()} {error.err_message}")
            return abort(
                error.code,
                message=ErrorResponse(error.code, error.err_message).get_json(),
            )
