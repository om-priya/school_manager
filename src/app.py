"""
This module contains code for configuration of app and also 
configuration with custom responses for generic erros
This module also registers the different routes to the app

This project aims to provide a management system for a school 
through which they can manage different entities in their school. 
The base assumption of this project is that it manages with the perspective of one school 
To check for super admin credentials go to /src/super_admin_meny.py 
"""

import logging
import os
import pymysql

from flask import Flask, request
from flask_smorest import Api
from shortuuid import ShortUUID

from database.database_access import DatabaseAccess
from models.response_format import ErrorResponse
from router.auth_router import blp as AuthRouter
from router.feedback_router import blp as FeedBackRouter
from router.event_router import blp as EventRouter
from router.issue_router import blp as IssueRouter
from router.principal_router import blp as PrincipalRouter
from router.teacher_router import blp as TeacherRouter
from router.user_router import blp as UserRouter
from router.leave_router import blp as LeaveRouter
from utils.custom_error import FailedValidation
from utils.initializer import initialize_app
from utils.set_app_config import set_app_config
from utils.jwt_exception_handler import jwt_exception_manager

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
    initialize_app()
    app = Flask(__name__)

    app = set_app_config(app)

    app.register_error_handler(
        400,
        lambda err: (ErrorResponse(400, str(err)).get_json(), 400),
    )
    app.register_error_handler(
        FailedValidation,
        lambda err: (ErrorResponse(422, str(err)).get_json(), 422),
    )
    app.register_error_handler(
        pymysql.Error,
        lambda err: (
            ErrorResponse(500, f"Something went wrong with db {str(err)}").get_json(),
            422,
        ),
    )
    app.register_error_handler(
        Exception,
        lambda error: (
            ErrorResponse(500, f"Something Went Wrong {error}").get_json(),
            500,
        ),
    )

    app = jwt_exception_manager(app)

    # creating the api instance which will used to register blueprint for the app
    api = Api(app)

    # setting req Id for logging
    @app.before_request
    def set_custom_headers():
        request_id = ShortUUID().random(length=10)
        request.environ["X-Request-Id"] = request_id

    @app.get("/api/v1/")
    def server_check():
        return {"server": "Is Up"}

    api.register_blueprint(AuthRouter)
    api.register_blueprint(FeedBackRouter)
    api.register_blueprint(EventRouter)
    api.register_blueprint(IssueRouter)
    api.register_blueprint(PrincipalRouter)
    api.register_blueprint(TeacherRouter)
    api.register_blueprint(UserRouter)
    api.register_blueprint(LeaveRouter)

    @app.delete("/api/v1/teardown")
    def teardown_test_db():
        if os.getenv("ENVIROMENT") == "test" and request.headers.get(
            "X-Token-Secret"
        ) == os.getenv("TOKEN_SECRET"):
            tables_names = DatabaseAccess.execute_returning_query("SHOW tables")
            for table_name in tables_names:
                DatabaseAccess.execute_non_returning_query(
                    f"DELETE FROM {table_name['Tables_in_testDb']}"
                )
            initialize_app()
            return {"message": "testDb Reset"}

        return {"message": "Hecker hai"}

    return app


flask_app = create_app()
