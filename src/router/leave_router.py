"""
File for leave router
"""
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required

from utils.role_checker_decorator import access_level
from controllers.leave_controller import LeavesController
from schema.leave_schema import LeaveIdSchema, LeaveSchema

blp = Blueprint(
    "Leave Router", __name__, url_prefix="/api/v1", description="Handling Leave Router"
)


@blp.route("/leaves")
class LeavesRouter(MethodView):
    """Class for handling /leaves endpoint"""

    @jwt_required()
    @access_level(["principal", "teacher"])
    def get(self):
        """get method on /leaves endpoint"""
        return LeavesController().get_leave_info()

    @jwt_required()
    @access_level(["principal", "teacher"])
    @blp.arguments(LeaveSchema)
    def post(self, leave_details):
        """post method on /leaves endpoint"""
        return LeavesController().apply_for_leave(leave_details)


@blp.route("/leaves/<string:leave_id>")
class ApproveLeaves(MethodView):
    """class for handling approve leave request"""

    @jwt_required()
    @access_level(["superadmin"])
    @blp.arguments(LeaveIdSchema, location="path")
    def put(self, leave_info, leave_id):
        """put method for approving leave"""
        return LeavesController().approve_leave(leave_info)
