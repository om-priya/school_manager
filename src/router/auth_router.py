"""File for Auth Router Endpoints"""

from flask_smorest import Blueprint
from flask.views import MethodView
from schema.auth_schema import LoginSchema, SignUpSchema
from controllers.auth_controller import AuthenticationController

# creating blueprint for the auth route which are login logout and signup
blp = Blueprint(
    "Auth_Route",
    __name__,
    url_prefix="/api/v1",
    description="Login, Logout and Signup Route",
)


@blp.route("/login")
class LoginRoute(MethodView):
    """Login Route"""

    @blp.arguments(LoginSchema)
    def post(self, login_details):
        """post method for /login"""
        return AuthenticationController.login_controller(login_details)


@blp.route("/logout")
class LogoutRoute(MethodView):
    """Logout Route"""

    def post(self):
        """post method for /logout"""
        return {"message": "Logout Successfully"}


@blp.route("/signup")
class SignUpRoute(MethodView):
    """SignUp Route"""

    @blp.arguments(SignUpSchema)
    def post(self, user_details):
        """post method for /signup"""
        return AuthenticationController.sign_up_controller(user_details)
