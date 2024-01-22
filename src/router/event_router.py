from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt
from flask_smorest import abort

from controllers.handlers.event_handler import EventHandler
from models.response_format import SuccessResponse, ErrorResponse
from utils.custom_error import DataNotFound
from utils.role_checker_decorator import access_level
from schema.event_schema import EventSchema

blp = Blueprint(
    "events",
    __name__,
    url_prefix="/api/v1",
    description="Events Router for School Project",
)


@blp.route("/events")
class EventRoute(MethodView):
    @jwt_required()
    @access_level(["teacher", "principal"])
    def get(self):
        try:
            jwt = get_jwt()
            user_id = jwt.get("sub").get("user_id")

            res_data = EventHandler(user_id).read_event()
            return SuccessResponse(
                200, "Here's the list of Events", res_data
            ).get_json()
        except DataNotFound:
            abort(404, message=ErrorResponse(404, "No Such Events Found").get_json())

    @jwt_required()
    @access_level(["principal"])
    @blp.arguments(EventSchema)
    def post(self, event_data):
        try:
            jwt = get_jwt()
            user_id = jwt.get("sub").get("user_id")

            EventHandler(user_id).create_event(event_data["event_message"])
        except Exception:
            abort(500, message=ErrorResponse(500, "Server Not Responding").get_json())
