"""
File for event router
"""

import logging
from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from controllers.event_controller import EventController
from utils.role_checker_decorator import access_level
from schema.event_schema import EventSchema
from helper.helper_function import get_request_id

blp = Blueprint(
    "events",
    __name__,
    url_prefix="/api/v1",
    description="Events Router for School Project",
)

logger = logging.getLogger(__name__)


@blp.route("/events")
class EventRoute(MethodView):
    """Class for handling /events endpoint"""

    @jwt_required()
    @access_level(["teacher", "principal"])
    def get(self):
        """get method on /events endpoint"""
        logger.info(f"{get_request_id()} hit /events get endpoint")
        return EventController().get_all_events()

    @jwt_required()
    @access_level(["principal"])
    @blp.arguments(EventSchema)
    def post(self, event_data):
        """post method on /events endpoint"""
        logger.info(f"{get_request_id()} hit /events post endpoint")
        return EventController().post_create_event(event_data)
