from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required

from utils.role_checker_decorator import access_level
from controllers.principal_controller import PrincipalController
from schema.principal_schema import PrincipalIdSchema

blp = Blueprint(
    "Principal Router",
    __name__,
    url_prefix="/api/v1",
    description="Router Handling Principla Routes",
)


@blp.route("/principals")
class GetAllPrincipals(MethodView):
    @jwt_required
    @access_level(["superadmin"])
    def get(self):
        return PrincipalController().get_all_principals()


@blp.route("/principal/<string:principal_id>")
class PrincipalById(MethodView):
    @jwt_required
    @access_level(["superadmin"])
    @blp.arguments(PrincipalIdSchema, location="path")
    def get(self, principal_info, principal_id):
        return PrincipalController().get_single_principal(
            principal_info["principal_id"]
        )

    @jwt_required
    @access_level(["superadmin"])
    @blp.arguments(PrincipalIdSchema, location="path")
    def delete(self, principal_info, principal_id):
        return PrincipalController().delete_principal(principal_info["principal_id"])


@blp.route("/principal/<string:principal_id>/approve")
class ApprovePrincipal(MethodView):
    @jwt_required
    @access_level(["superadmin"])
    @blp.arguments(PrincipalIdSchema, location="path")
    def put(self, principal_info, principal_id):
        return PrincipalController().approve_principal(principal_info["principal_id"])
