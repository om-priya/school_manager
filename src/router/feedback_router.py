from flask_smorest import Blueprint, abort
from flask import jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt

from models.response_format import ErrorResponse, SuccessResponse
from schema.feedback_schema import FeedbackSchema, FeedbackTeacherIdSchema
from utils.role_checker_decorator import access_level
from utils.custom_error import DataNotFound
from controllers.feedback_controller import FeedbackController
from handlers.feedback_handler import FeedbackHandler

blp = Blueprint(
    "FeedBack_Router", __name__, url_prefix="/api/v1", description="Feedback router"
)


@blp.route("/feedbacks")
class GetFeedBacks(MethodView):
    @jwt_required
    @access_level(["teacher", "principal"])
    def get(self):
        return FeedbackController().get_all_feedbacks()

@blp.route("/feedbacks/<string:teacher_id>")
class GetFeedBacksById(MethodView):
    @jwt_required
    @access_level(["principal"])
    @blp.arguments(FeedbackSchema)
    @blp.arguments(FeedbackTeacherIdSchema, location="path")
    def post(self, feedback_info, teacher, teacher_id):
        return FeedbackController().give_teacher_feedback(
            teacher["teacher_id"], feedback_info
        )
