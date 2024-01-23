from flask import Flask
from flask_jwt_extended import JWTManager
from flask_smorest import Api, abort
from models.response_format import ErrorResponse

import logging

from router.auth_router import blp as AuthRouter
from router.feedback_router import blp as FeedBackRouter
from router.event_router import blp as EventRouter


def create_app():
    """
    This Function will create the server for my project
    """

    # creating flask app instance with default configuration
    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "School Management System REST API"
    app.config["API_VERSION"] = "v1"
    app.config["APPLICATION_ROOT"] = "/school"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/api-docs"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["JWT_SECRET_KEY"] = "dbeywbsakxwj903jdsnxkcjdbdsmxxdionsalxlsakcufvdcd"

    @app.errorhandler(Exception)
    def all_exception_handler(error):
        logging.exception(error)
        abort(500, message=ErrorResponse(500, "Server Not Responding").get_json())

    # create jwtmanager instance which will handle all the jwt related logic
    jwt = JWTManager(app)

    # creating the api instance which will used to register blueprint for the app
    api = Api(app)

    api.register_blueprint(AuthRouter)
    api.register_blueprint(FeedBackRouter)
    api.register_blueprint(EventRouter)
    return app
