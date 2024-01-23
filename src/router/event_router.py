from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt
from flask_smorest import abort

from handlers.event_handler import EventHandler
from controllers.event_controller import EventController
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
        return EventController().get_all_events()

    @jwt_required()
    @access_level(["principal"])
    @blp.arguments(EventSchema)
    def post(self, event_data):
        return EventController().post_create_event(event_data)
