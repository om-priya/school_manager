"""
File for principal router
"""

import logging
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required

from utils.role_checker_decorator import access_level
from controllers.principal_controller import PrincipalController
from schema.principal_schema import PrincipalIdSchema, PrincipalDetails
from helper.helper_function import get_request_id

blp = Blueprint(
    "Principal Router",
    __name__,
    url_prefix="/api/v1",
    description="Router Handling Principla Routes",
)

logger = logging.getLogger(__name__)


@blp.route("/principals")
class GetAllPrincipals(MethodView):
    """Class for handling /principals endpoint"""

    @jwt_required()
    @access_level(["superadmin"])
    def get(self):
        """get method on /principals endpoint"""
        logger.info(f"{get_request_id()} hit /principals get endpoint")
        return PrincipalController().get_all_principals()


@blp.route("/principals/<string:principal_id>")
class PrincipalById(MethodView):
    """Class for handling /principals/principal_id endpoint"""

    @jwt_required()
    @access_level(["superadmin"])
    @blp.arguments(PrincipalIdSchema, location="path")
    def get(self, principal_info, principal_id):
        """get method on /principals/principal_id endpoint"""
        logger.info(f"{get_request_id()} hit /principals/principal_id get endpoint")
        return PrincipalController().get_single_principal(
            principal_info["principal_id"]
        )

    @jwt_required()
    @access_level(["superadmin"])
    @blp.arguments(PrincipalIdSchema, location="path")
    @blp.arguments(PrincipalDetails)
    def put(self, principal_info, principal_updated_details, principal_id):
        """get method on /principals/principal_id endpoint"""
        logger.info(f"{get_request_id()} hit /principals/principal_id put endpoint")
        return PrincipalController().update_principal_controller(
            principal_info["principal_id"], principal_updated_details
        )

    @jwt_required()
    @access_level(["superadmin"])
    @blp.arguments(PrincipalIdSchema, location="path")
    def delete(self, principal_id_obj, principal_id):
        """delete method on /principals/principal_id endpoint"""
        logger.info(f"{get_request_id()} hit /principals/principal_id delete endpoint")
        return PrincipalController().delete_principal(principal_id_obj["principal_id"])


@blp.route("/principals/<string:principal_id>/approve")
class ApprovePrincipal(MethodView):
    """class for handling approve principal endpoint"""

    @jwt_required()
    @access_level(["superadmin"])
    @blp.arguments(PrincipalIdSchema, location="path")
    def put(self, principal_info, principal_id):
        """put method on /principals/principal_id/approve endpoint"""
        logger.info(
            f"{get_request_id()} hit /principals/principal_id/approve put endpoint"
        )
        return PrincipalController().approve_principal(principal_info["principal_id"])
