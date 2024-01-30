"""
File for issue router
"""
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required

from utils.role_checker_decorator import access_level
from controllers.issue_controller import IssueController
from schema.issue_schema import IssueSchema

blp = Blueprint(
    "Issue Router", __name__, url_prefix="/api/v1", description="Issue Handler Router"
)


@blp.route("/issues")
class Issues(MethodView):
    """Class for handling /issues endpoint"""

    @jwt_required()
    @access_level(["principal"])
    def get(self):
        """get method on /issues endpoint"""
        return IssueController().get_all_issues()

    @jwt_required()
    @access_level(["teacher"])
    @blp.arguments(IssueSchema)
    def post(self, issue_mssg):
        """post method on /issues endpoint"""
        return IssueController().create_issue_controller(issue_mssg)
