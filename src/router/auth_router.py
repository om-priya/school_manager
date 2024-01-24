from flask import jsonify
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import create_access_token
from schema.auth_schema import LoginSchema, SignUpSchema
from models.response_format import ErrorResponse, SuccessResponse
import mysql.connector

from controllers.auth_controller import AuthenticationController
from utils.custom_error import DataNotFound, InvalidCredentials, NotActive

# creating blueprint for the auth route which are login logout and signup
blp = Blueprint("Auth_Route", __name__, description="Login, Logout and Signup Route")


@blp.route("/login")
class LoginRoute(MethodView):
    @blp.arguments(LoginSchema)
    def post(self, login_details):
        return AuthenticationController.login_controller(login_details)


@blp.route("/logout")
class LogoutRoute(MethodView):
    def post(self):
        return {"message": "Logout Successfully"}


@blp.route("/signup")
class SignUpRoute(MethodView):
    @blp.arguments(SignUpSchema)
    def post(self, user_details):
        return AuthenticationController.sign_up_controller(user_details)
