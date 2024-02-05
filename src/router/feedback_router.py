"""
Files for handling feedback routes
"""

import logging
from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from schema.feedback_schema import FeedbackSchema, FeedbackTeacherIdSchema
from utils.role_checker_decorator import access_level
from controllers.feedback_controller import FeedbackController
from helper.helper_function import get_request_id

blp = Blueprint(
    "FeedBack_Router", __name__, url_prefix="/api/v1", description="Feedback router"
)

logger = logging.getLogger(__name__)


@blp.route("/feedbacks")
class GetFeedBacks(MethodView):
    """Class for handling /feedbacks endpoint"""

    @jwt_required()
    @access_level(["teacher", "principal"])
    def get(self):
        """get method on /feedbacks endpoint"""
        logger.info(f"{get_request_id()} hit /feedbacks get endpoint")
        return FeedbackController().get_all_feedbacks()


@blp.route("/feedbacks/<string:teacher_id>")
class GetFeedBacksById(MethodView):
    """Class for handling /feedbacks/teacher_id endpoint"""

    @jwt_required()
    @access_level(["principal"])
    @blp.arguments(FeedbackSchema)
    @blp.arguments(FeedbackTeacherIdSchema, location="path")
    def post(self, feedback_info, teacher, teacher_id):
        """post method on /feedbacks/teacher_id endpoint"""
        logger.info(f"{get_request_id()} hit /feedbacks/teacher_id post endpoint")
        return FeedbackController().give_teacher_feedback(
            teacher["teacher_id"], feedback_info
        )
