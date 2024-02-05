""" This module is responsible for handling all the controlers for principal """

from flask_smorest import abort
from utils.custom_error import DataNotFound, AlreadyPresent
from models.response_format import SuccessResponse, ErrorResponse
from handlers.principal_handler import PrincipalHandler
import logging

logger = logging.getLogger(__name__)


class PrincipalController:
    def get_all_principals(self):
        try:
            res_data = PrincipalHandler().get_all_principal()
            return SuccessResponse(200, "List of Principals", res_data).get_json()
        except DataNotFound:
            return abort(
                404, message=ErrorResponse(404, "No Principal Found").get_json()
            )

    def get_single_principal(self, principal_id):
        try:
            res_data = PrincipalHandler().get_principal_by_id(principal_id)
            return SuccessResponse(200, "List of Principal", res_data).get_json()
        except DataNotFound:
            return abort(
                404,
                message=ErrorResponse(
                    404, "No Principal with given Id Found"
                ).get_json(),
            )

    def approve_principal(self, principal_id):
        try:
            PrincipalHandler().approve_principal(principal_id)
            return SuccessResponse(200, "Principal Approved Successfully").get_json()
        except DataNotFound:
            return abort(
                404,
                message=ErrorResponse(
                    404, "No Principal with given Id Found"
                ).get_json(),
            )
        except AlreadyPresent:
            return abort(
                409, message=ErrorResponse(409, "Principal Already Present").get_json()
            )

    def delete_principal(self, principal_id):
        try:
            PrincipalHandler().delete_principal(principal_id)
            return SuccessResponse(200, "Principal Deleted SuccessFully").get_json()
        except DataNotFound:
            return abort(
                404,
                message=ErrorResponse(
                    404, "No Principal with given Id Found"
                ).get_json(),
            )
