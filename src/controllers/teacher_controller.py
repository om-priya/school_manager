""" This Module Contains all the functionality that a teacher can perform """

import logging
from flask_smorest import abort

from utils.custom_error import DataNotFound, FailedAction
from models.response_format import SuccessResponse, ErrorResponse
from handlers.teacher_handler import TeacherHandler
from config.display_menu import PromptMessage
from helper.helper_function import get_request_id

logger = logging.getLogger(__name__)


class TeacherController:
    def get_all_teacher(self):
        try:
            logger.info(f"{get_request_id()} Calling handler for getting all teachers")
            res_data = TeacherHandler().get_all_teacher()
            logger.info(f"{get_request_id()} formatting response after getting details")
            return SuccessResponse(
                200, PromptMessage.LIST_ENTRY.format("Teachers"), res_data
            ).get_json()
        except DataNotFound:
            logger.info(f"{get_request_id()} formatting response for no teacher found")
            return abort(
                404,
                message=ErrorResponse(
                    404, PromptMessage.NOTHING_FOUND.format("Teachers")
                ).get_json(),
            )

    def get_single_teacher(self, teacher_id):
        try:
            logger.info(f"{get_request_id()} Calling handler for getting teacher by id")
            res_data = TeacherHandler().get_teacher_by_id(teacher_id)
            logger.info(f"{get_request_id()} formatting response after getting details")
            return SuccessResponse(
                200, PromptMessage.LIST_ENTRY.format("Teacher"), res_data
            ).get_json()
        except DataNotFound:
            logger.info(f"{get_request_id()} formatting response for no teacher found")
            return abort(
                404,
                message=ErrorResponse(
                    404, PromptMessage.NOTHING_FOUND.format("Teacher")
                ).get_json(),
            )

    def approve_teacher(self, teacher_id):
        try:
            logger.info(f"{get_request_id()} Calling handler for approving teacher")
            TeacherHandler().approve_teacher(teacher_id)
            logger.info(
                f"{get_request_id()} formatting response after successfull approval"
            )
            return SuccessResponse(
                200, PromptMessage.APPROVE_SUCCESS.format("Teacher")
            ).get_json()
        except DataNotFound:
            logger.info(f"{get_request_id()} formatting response for no teacher found")
            return abort(
                404,
                message=ErrorResponse(
                    404, PromptMessage.NOTHING_FOUND.format("Teacher")
                ).get_json(),
            )
        except FailedAction:
            logger.info(
                f"{get_request_id()} Can't approve principal with id {teacher_id}"
            )
            return abort(
                409,
                message=ErrorResponse(
                    409, PromptMessage.APPROVE_FAILED.format("Teacher")
                ).get_json(),
            )

    def delete_teacher(self, teacher_id):
        try:
            logger.info(f"{get_request_id()} Calling handler for deleting teacher")
            TeacherHandler().delete_teacher(teacher_id)
            logger.info(f"{get_request_id()} fromating response after deleting teacher")
            return SuccessResponse(
                200, PromptMessage.SUCCESS_ACTION.format("Teacher deleted")
            ).get_json()
        except DataNotFound:
            logger.info(
                f"{get_request_id()} formatting response for no teacher found to delete with id {teacher_id}"
            )
            return abort(
                404,
                message=ErrorResponse(
                    404, PromptMessage.NOTHING_FOUND.format("Teacher")
                ).get_json(),
            )
