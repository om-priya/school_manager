"""
File for user router
"""

import logging
from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from controllers.user_controller import UserController
from utils.role_checker_decorator import access_level
from schema.user_schema import ChangePasswordSchema
from helper.helper_function import get_request_id

blp = Blueprint(
    "User Router",
    __name__,
    url_prefix="/api/v1/user",
    description="Common end points for all users",
)

logger = logging.getLogger(__name__)


@blp.route("/profile")
class MyProfile(MethodView):
    """Class for handling /profile endpoint"""

    @jwt_required()
    @access_level(["teacher", "principal"])
    def get(self):
        """get method on /profile endpoint"""
        logger.info(f"{get_request_id()} hit /profile get endpoint")
        return UserController().get_my_profile()


@blp.route("/salary-history")
class MySalaryHistory(MethodView):
    """Class for handling /salary-history endpoint"""

    @jwt_required()
    @access_level(["teacher", "principal"])
    def get(self):
        """get method on /salary-history endpoint"""
        logger.info(f"{get_request_id()} hit /salary-history get endpoint")
        return UserController().get_my_salary_history()


@blp.route("/change-password")
class ChangePassword(MethodView):
    """Class for handling /change-password endpoint"""

    @jwt_required()
    @access_level(["teacher", "principal"])
    @blp.arguments(ChangePasswordSchema)
    def post(self, change_password_details):
        """post method on /change-password endpoint"""
        logger.info(f"{get_request_id()} hit /change-password post endpoint")
        return UserController().change_password(change_password_details)
