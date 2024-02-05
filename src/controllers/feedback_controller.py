from handlers.feedback_handler import FeedbackHandler
from flask_smorest import abort
from models.response_format import SuccessResponse, ErrorResponse
from utils.custom_error import DataNotFound
from helper.helper_function import get_user_id_from_jwt


class FeedbackController:
    def get_all_feedbacks(self):
        try:
            user_id = get_user_id_from_jwt()

            res_data = FeedbackHandler(user_id).read_feedback()
            return SuccessResponse(
                200, "Here's the list of feedback", res_data
            ).get_json()
        except DataNotFound:
            return abort(
                404, message=ErrorResponse(404, "No Such Feedbacks Found").get_json()
            )

    def give_teacher_feedback(self, teacher_id, feedback_info):
        try:
            user_id = get_user_id_from_jwt()

            FeedbackHandler(user_id).give_feedback(
                teacher_id, feedback_info["feedback_message"]
            )
            return SuccessResponse(200, "FeedBack Added Successfully").get_json()
        except DataNotFound:
            return abort(404, message=ErrorResponse(404, "No Teacher Found").get_json())
