""" This module is responsible for handling all the controlers for principal """

from flask_smorest import abort
from utils.custom_error import DataNotFound, AlreadyPresent
from models.response_format import SuccessResponse, ErrorResponse
from handlers.principal_handler import PrincipalHandler
from helper.helper_function import get_request_id
from config.display_menu import PromptMessage
import logging

logger = logging.getLogger(__name__)


class PrincipalController:
    def get_all_principals(self):
        try:
            logger.info(
                f"{get_request_id()} Calling handler for getting all principals"
            )
            res_data = PrincipalHandler().get_all_principal()
            logger.info(f"{get_request_id()} formatting response after getting details")
            return SuccessResponse(
                200, PromptMessage.LIST_ENTRY.format("Principals"), res_data
            ).get_json()
        except DataNotFound:
            logger.info(
                f"{get_request_id()} formatting response for no principal found"
            )
            return abort(
                404,
                message=ErrorResponse(
                    404, PromptMessage.NOTHING_FOUND.format("Principal")
                ).get_json(),
            )

    def get_single_principal(self, principal_id):
        try:
            logger.info(
                f"{get_request_id()} Calling handler for getting principal by id"
            )
            res_data = PrincipalHandler().get_principal_by_id(principal_id)
            logger.info(f"{get_request_id()} formatting response after getting details")
            return SuccessResponse(
                200, PromptMessage.LIST_ENTRY.format("Principal"), res_data
            ).get_json()
        except DataNotFound:
            logger.info(
                f"{get_request_id()} formatting response for no principal found"
            )
            return abort(
                404,
                message=ErrorResponse(
                    404, PromptMessage.NOTHING_FOUND.format("Principal")
                ).get_json(),
            )

    def approve_principal(self, principal_id):
        try:
            logger.info(f"{get_request_id()} Calling handler for approving principal")
            PrincipalHandler().approve_principal(principal_id)
            logger.info(
                f"{get_request_id()} formatting response after successfull approval"
            )
            return SuccessResponse(
                200, PromptMessage.APPROVE_SUCCESS.format("Principal")
            ).get_json()
        except DataNotFound:
            logger.info(
                f"{get_request_id()} formatting response for no principal found"
            )
            return abort(
                404,
                message=ErrorResponse(
                    404, PromptMessage.NOTHING_FOUND.format("Principal")
                ).get_json(),
            )
        except AlreadyPresent:
            logger.info(f"{get_request_id()} Tried to add more than one principal")
            return abort(
                409,
                message=ErrorResponse(
                    409, PromptMessage.ALREADY_EXITS.format("Principal")
                ).get_json(),
            )

    def delete_principal(self, principal_id):
        try:
            logger.info(f"{get_request_id()} Calling handler for deleting principal")
            PrincipalHandler().delete_principal(principal_id)
            logger.info(
                f"{get_request_id()} fromating response after deleting principal"
            )
            return SuccessResponse(
                200, PromptMessage.SUCCESS_ACTION.format("Principal Deleted")
            ).get_json()
        except DataNotFound:
            logger.info(
                f"{get_request_id()} formatting response for no principal found to delete with id {principal_id}"
            )
            return abort(
                404,
                message=ErrorResponse(
                    404, PromptMessage.NOTHING_FOUND.format("Principal")
                ).get_json(),
            )
