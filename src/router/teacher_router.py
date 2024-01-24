from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from controllers.teacher_controller import TeacherController
from utils.role_checker_decorator import access_level
from schema.teacher_schema import TeacherIdSchema

blp = Blueprint(
    "Teacher Router",
    __name__,
    url_prefix="/api/v1",
    description="Router Handling Teacher Route",
)


@blp.route("/teachers")
class GetAllTeachers(MethodView):
    @jwt_required
    @access_level(["principal"])
    def get(self):
        return TeacherController().get_all_teacher()


@blp.route("/teachers/<string:teacher_id>")
class TeachersById(MethodView):
    @jwt_required
    @access_level(["principal"])
    @blp.arguments(TeacherIdSchema, location="path")
    def get(self, teacher_info, teacher_id):
        return TeacherController().get_single_teacher(teacher_info["teacher_id"])

    @jwt_required
    @access_level(["principal"])
    @blp.arguments(TeacherIdSchema, location="path")
    def delete(self, teacher_info, teacher_id):
        return TeacherController().delete_teacher(teacher_info["teacher_id"])


@blp.route("/teachers/<string:teacher_id>/approve")
class ApproveTeacher(MethodView):
    @jwt_required
    @access_level(["principal"])
    @blp.arguments(TeacherIdSchema, location="path")
    def put(self, teacher_info, teacher_id):
        return TeacherController().approve_teacher(teacher_info["teacher_id"])
