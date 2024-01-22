from flask import jsonify
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import create_access_token
from schema.auth_schema import LoginSchema, SignUpSchema
from models.response_format import ErrorResponse, SuccessResponse
import mysql.connector

from controllers.user_controller import AuthenticationController
from utils.custom_error import DataNotFound, InvalidCredentials, NotActive

# creating blueprint for the auth route which are login logout and signup
blp = Blueprint("Auth_Route", __name__, description="Login, Logout and Signup Route")


@blp.route("/login")
class LoginRoute(MethodView):
    @blp.arguments(LoginSchema)
    def post(self, login_details):
        try:
            # user_details -> success, user_id, role
            user_details = AuthenticationController.is_logged_in(
                login_details["user_name"], login_details["password"]
            )
            access_token = create_access_token(
                identity={"user_id": user_details[1], "role": user_details[2]}
            )
            return SuccessResponse(
                200,
                "User Logged In SuccessFully",
                {"access_token": access_token},
            ).get_json()

        except InvalidCredentials:
            return abort(
                401,
                message=ErrorResponse(
                    401, "Username or Passwrod is Incorrect"
                ).get_json(),
            )
        except NotActive:
            return abort(
                403,
                message=ErrorResponse(
                    403, "You Don't have access to the platform"
                ).get_json(),
            )
        except DataNotFound:
            return abort(404, message=ErrorResponse(404, "User Not Found").get_json())


@blp.route("/logout")
class LogoutRoute(MethodView):
    def post(self):
        return {"messgae": "Logout Successfully"}


@blp.route("/signup")
class SignUpRoute(MethodView):
    @blp.arguments(SignUpSchema)
    def post(self, user_details):
        try:
            AuthenticationController.sign_up(user_details)
            return SuccessResponse(
                200, "User Signed Up SuccessFully wait for Approval"
            ).get_json()
        except mysql.connector.IntegrityError:
            return abort(
                409, message=ErrorResponse(409, "User Already Exists").get_json()
            )
        except Exception:
            return abort(
                500, message=ErrorResponse(500, "Server Not Responding").get_json()
            )
