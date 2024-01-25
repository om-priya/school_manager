""" This Module Contains all the functionality that a teacher can perform """
import logging
from flask_smorest import abort

from utils.custom_error import DataNotFound, FailedAction
from models.response_format import SuccessResponse, ErrorResponse
from handlers.teacher_handler import TeacherHandler

logger = logging.getLogger(__name__)


class TeacherController:
    def get_all_teacher(self):
        try:
            res_data = TeacherHandler().get_all_teacher()
            return SuccessResponse(200, "Here's the list of Teachers", res_data).get_json()
        except DataNotFound:
            return abort(404, message=ErrorResponse(404, "No Teachers Found").get_json())

    def get_single_teacher(self, teacher_id):
        try:
            res_data = TeacherHandler().get_teacher_by_id(teacher_id)
            return SuccessResponse(200, "Here's the details of Teacher", res_data).get_json()
        except DataNotFound:
            return abort(404, message=ErrorResponse(404, "No Teacher Found").get_json())

    def approve_teacher(self, teacher_id):
        try:
            TeacherHandler().approve_teacher(teacher_id)
            return SuccessResponse(200, "Teacher Approved Successfully").get_json()
        except DataNotFound:
            return abort(404, message=ErrorResponse(404, "No Teacher Found").get_json())
        except FailedAction:
            return abort(409, message=ErrorResponse(409, "Teacher Can't be Approved").get_json())

    def delete_teacher(self, teacher_id):
        try:
            TeacherHandler().delete_teacher(teacher_id)
            return SuccessResponse(200, "Teacher Deletd").get_json()
        except DataNotFound:
            return abort(404, message=ErrorResponse(404, "No Teacher Found").get_json())
