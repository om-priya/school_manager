from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required

from utils.role_checker_decorator import access_level
from controllers.leave_controller import LeavesController
from schema.leave_schema import LeaveIdSchema

blp = Blueprint(
    "Leave Router", __name__, url_prefix="/api/v1", description="Handling Leave Router"
)


@blp.route("/leaves")
class LeavesRouter(MethodView):
    @jwt_required
    @access_level(["principal", "teacher"])
    def get(self):
        return LeavesController().get_leave_info()

    @jwt_required
    @access_level(["principal", "teacher"])
    def post(self):
        return LeavesController().apply_for_leave()


@blp.route("/leaves/<string:leave_id>")
class ApproveLeaves(MethodView):
    @jwt_required
    @access_level(["superadmin"])
    @blp.arguments(LeaveIdSchema, location="path")
    def put(self, leave_info, leave_id):
        return LeavesController().approve_leave(leave_info)
