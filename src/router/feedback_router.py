from flask_smorest import Blueprint, abort
from flask import jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt

from models.response_format import ErrorResponse, SuccessResponse
from utils.role_checker_decorator import access_level
from utils.custom_error import DataNotFound
from controllers.handlers.feedback_handler import FeedbackHandler

blp = Blueprint(
    "FeedBack_Router", __name__, url_prefix="/api/v1", description="Feedback router"
)


@blp.route("/feedbacks")
class GetFeedBacks(MethodView):
    @jwt_required
    @access_level(["teacher", "principal"])
    def get(self):
        try:
            jwt = get_jwt()
            user_id = jwt.get("sub").get("user_id")

            res_data = FeedbackHandler(user_id).read_feedback()
            return SuccessResponse(200, "Here's the list of feedback", res_data)
        except DataNotFound:
            return abort(
                404, message=ErrorResponse(404, "No Such Feedbacks Found").get_json()
            )


@blp.route("/feedbacks/{teacher_id}")
class GetFeedBacksById(MethodView):
    @jwt_required
    @access_level(["principal"])
    def post(self, teacher_id):
        return {"message": "feedback", "teacher_id": teacher_id}
