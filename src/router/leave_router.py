"""
File for leave router
"""

import logging
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required

from utils.role_checker_decorator import access_level
from controllers.leave_controller import LeavesController
from schema.leave_schema import LeaveIdSchema, LeaveSchema
from helper.helper_function import get_request_id

blp = Blueprint(
    "Leave Router", __name__, url_prefix="/api/v1", description="Handling Leave Router"
)

logger = logging.getLogger(__name__)


@blp.route("/leaves")
class LeavesRouter(MethodView):
    """Class for handling /leaves endpoint"""

    @jwt_required()
    @access_level(["superadmin", "principal", "teacher"])
    def get(self):
        """get method on /leaves endpoint"""
        logger.info(f"{get_request_id()} hit /leaves get endpoint")
        return LeavesController().get_leave_info()

    @jwt_required()
    @access_level(["principal", "teacher"])
    @blp.arguments(LeaveSchema)
    def post(self, leave_details):
        """post method on /leaves endpoint"""
        logger.info(f"{get_request_id()} hit /leaves post endpoint")
        return LeavesController().apply_for_leave(leave_details)


@blp.route("/leaves/<string:leave_id>")
class ApproveLeaves(MethodView):
    """class for handling approve leave request"""

    @jwt_required()
    @access_level(["superadmin"])
    @blp.arguments(LeaveIdSchema, location="path")
    def put(self, leave_info, leave_id):
        """put method for approving leave"""
        logger.info(f"{get_request_id()} hit /leaves/leave_id put endpoint")
        return LeavesController().approve_leave(leave_info)
