"""This module contains code for configuration of app and also 
configuration with custom responses for generic erros
This module also registers the different routes to the app"""
import logging

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from models.response_format import ErrorResponse

from router.auth_router import blp as AuthRouter
from router.feedback_router import blp as FeedBackRouter
from router.event_router import blp as EventRouter
from router.issue_router import blp as IssueRouter
from router.principal_router import blp as PrincipalRouter
from router.teacher_router import blp as TeacherRouter
from router.user_router import blp as UserRouter
from utils.custom_error import FailedValidation

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
    level=logging.DEBUG,
    filename="logs.log",
)


def create_app():
    """
    This Function will create the server for my project
    It also registers different routes with the application

    (parameters) :-> None

    (returns) :-> app instance made with Flask
    """

    # creating flask app instance with default configuration
    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "School Management System REST API"
    app.config["API_VERSION"] = "v1"
    app.config["APPLICATION_ROOT"] = "/"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/api-docs"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["JWT_SECRET_KEY"] = "dbeywbsakxwj903jdsnxkcjdbdsmxxdionsalxlsakcufvdcd"

    app.register_error_handler(
        FailedValidation,
        lambda err: (ErrorResponse(422, str(err)).get_json(), 422),
    )
    app.register_error_handler(
        Exception,
        lambda _: (ErrorResponse(500, "Something Went Wrong").get_json(), 500),
    )

    # create jwtmanager instance which will handle all the jwt related logic
    jwt = JWTManager(app)

    # custom errors for jwt failure
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(_jwt_header, jwt_payload):
        pass

    @jwt.revoked_token_loader
    def revoked_token_callback(_jwt_header, _jwt_payload):
        return (ErrorResponse(401, "Token is Revoked").get_json(), 401)

    @jwt.expired_token_loader
    def expired_token_callback(_jwt_header, _jwt_payload):
        return (ErrorResponse(401, "Token is Not Valid").get_json(), 401)

    @jwt.unauthorized_loader
    def missing_token_callback(_error):
        return (ErrorResponse(401, "Token is Missing").get_json(), 401)

    @jwt.invalid_token_loader
    def invalid_token_callback(_error):
        return (ErrorResponse(401, "Invalid Token Provided").get_json(), 401)

    # creating the api instance which will used to register blueprint for the app
    api = Api(app)

    api.register_blueprint(AuthRouter)
    api.register_blueprint(FeedBackRouter)
    api.register_blueprint(EventRouter)
    api.register_blueprint(IssueRouter)
    api.register_blueprint(PrincipalRouter)
    api.register_blueprint(TeacherRouter)
    api.register_blueprint(UserRouter)
    return app
