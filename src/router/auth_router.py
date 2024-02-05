"""File for Auth Router Endpoints"""

import logging
from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from schema.auth_schema import LoginSchema, SignUpSchema
from controllers.auth_controller import AuthenticationController
from helper.helper_function import get_request_id

# creating blueprint for the auth route which are login logout and signup
blp = Blueprint(
    "Auth_Route",
    __name__,
    url_prefix="/api/v1",
    description="Login, Logout and Signup Route",
)

logger = logging.getLogger(__name__)


@blp.route("/login")
class LoginRoute(MethodView):
    """Login Route"""

    @blp.arguments(LoginSchema)
    def post(self, login_details):
        """post method for /login"""
        logger.info(f"{get_request_id()} hit /login post endpoint")
        return AuthenticationController.login_controller(login_details)


@blp.route("/logout")
class LogoutRoute(MethodView):
    """Logout Route"""

    @jwt_required()
    def post(self):
        """post method for /logout"""
        logger.info(f"{get_request_id()} hit /logout post endpoint")
        return AuthenticationController.logout_controller()


@blp.route("/signup")
class SignUpRoute(MethodView):
    """SignUp Route"""

    @blp.arguments(SignUpSchema)
    def post(self, user_details):
        """post method for /signup"""
        logger.info(f"{get_request_id()} hit /signup post endpoint")
        return AuthenticationController.sign_up_controller(user_details)
