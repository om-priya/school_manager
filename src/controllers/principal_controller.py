""" This module is responsible for handling all the controlers for principal """

from flask_smorest import abort
from utils.custom_error import DataNotFound, AlreadyPresent
from models.response_format import SuccessResponse, ErrorResponse
from handlers.principal_handler import PrincipalHandler
from config.display_menu import PromptMessage
import logging

logger = logging.getLogger(__name__)


class PrincipalController:
    def get_all_principals(self):
        try:
            res_data = PrincipalHandler().get_all_principal()
            return SuccessResponse(
                200, PromptMessage.LIST_ENTRY.format("Principals"), res_data
            ).get_json()
        except DataNotFound:
            return abort(
                404,
                message=ErrorResponse(
                    404, PromptMessage.NOTHING_FOUND.format("Principal")
                ).get_json(),
            )

    def get_single_principal(self, principal_id):
        try:
            res_data = PrincipalHandler().get_principal_by_id(principal_id)
            return SuccessResponse(
                200, PromptMessage.LIST_ENTRY.format("Principal"), res_data
            ).get_json()
        except DataNotFound:
            return abort(
                404,
                message=ErrorResponse(
                    404, PromptMessage.NOTHING_FOUND.format("Principal")
                ).get_json(),
            )

    def approve_principal(self, principal_id):
        try:
            PrincipalHandler().approve_principal(principal_id)
            return SuccessResponse(
                200, PromptMessage.APPROVE_SUCCESS.format("Principal")
            ).get_json()
        except DataNotFound:
            return abort(
                404,
                message=ErrorResponse(
                    404, PromptMessage.NOTHING_FOUND.format("Principal")
                ).get_json(),
            )
        except AlreadyPresent:
            return abort(
                409,
                message=ErrorResponse(
                    409, PromptMessage.ALREADY_EXITS.format("Principal")
                ).get_json(),
            )

    def delete_principal(self, principal_id):
        try:
            PrincipalHandler().delete_principal(principal_id)
            return SuccessResponse(
                200, PromptMessage.SUCCESS_ACTION.format("Principal Deleted")
            ).get_json()
        except DataNotFound:
            return abort(
                404,
                message=ErrorResponse(
                    404, PromptMessage.NOTHING_FOUND.format("Principal")
                ).get_json(),
            )
