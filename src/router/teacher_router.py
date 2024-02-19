"""
File for teacher router
"""

import logging
from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from controllers.teacher_controller import TeacherController
from utils.role_checker_decorator import access_level
from schema.teacher_schema import TeacherIdSchema, TeacherDetails
from helper.helper_function import get_request_id

blp = Blueprint(
    "Teacher Router",
    __name__,
    url_prefix="/api/v1",
    description="Router Handling Teacher Route",
)

logger = logging.getLogger(__name__)


@blp.route("/teachers")
class GetAllTeachers(MethodView):
    """Class for handling /teachers endpoint"""

    @jwt_required()
    @access_level(["principal"])
    def get(self):
        """get method on /teachers endpoint"""
        logger.info(f"{get_request_id()} hit /teachers get endpoint")
        return TeacherController().get_all_teacher()


@blp.route("/teachers/<string:teacher_id>")
class TeachersById(MethodView):
    """Class for handling /teachers/teacher_id endpoint"""

    @jwt_required()
    @access_level(["principal"])
    @blp.arguments(TeacherIdSchema, location="path")
    def get(self, teacher_info, teacher_id):
        """get method on /teachers/teacher_id endpoint"""
        logger.info(f"{get_request_id()} hit /teachers/teachers_id get endpoint")
        return TeacherController().get_single_teacher(teacher_info["teacher_id"])

    @jwt_required()
    @access_level(["principal"])
    @blp.arguments(TeacherIdSchema, location="path")
    @blp.arguments(TeacherDetails)
    def put(self, teacher_info, teacher_details, teacher_id):
        """get method on /teachers/teacher_id endpoint"""
        logger.info(f"{get_request_id()} hit /teachers/teachers_id get endpoint")
        return TeacherController().update_teacher_controller(teacher_info["teacher_id"], teacher_details)

    @jwt_required()
    @access_level(["principal"])
    @blp.arguments(TeacherIdSchema, location="path")
    def delete(self, teacher_info, teacher_id):
        """delete method on /teachers/teacher_id endpoint"""
        logger.info(f"{get_request_id()} hit /teachers/teachers_id delete endpoint")
        return TeacherController().delete_teacher(teacher_info["teacher_id"])


@blp.route("/teachers/<string:teacher_id>/approve")
class ApproveTeacher(MethodView):
    """class for handling approve teacher endpoint"""

    @jwt_required()
    @access_level(["principal"])
    @blp.arguments(TeacherIdSchema, location="path")
    def put(self, teacher_info, teacher_id):
        """put method on /teachers/teacher_id/approve endpoint"""
        logger.info(
            f"{get_request_id()} hit /teachers/teachers_id/approve put endpoint"
        )
        return TeacherController().approve_teacher(teacher_info["teacher_id"])
