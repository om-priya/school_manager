from handlers.event_handler import EventHandler
from flask_smorest import abort
from helper.helper_function import get_user_id_from_jwt
from models.response_format import SuccessResponse, ErrorResponse
from utils.custom_error import DataNotFound


class EventController:
    def get_all_events(self):
        try:
            user_id = get_user_id_from_jwt()

            res_data = EventHandler(user_id).read_event()
            return SuccessResponse(
                200, "Here's the list of Events", res_data
            ).get_json()
        except DataNotFound:
            return abort(
                404, message=ErrorResponse(404, "No Such Events Found").get_json()
            )

    def post_create_event(self, event_data):
        user_id = get_user_id_from_jwt()

        EventHandler(user_id).create_event(event_data["event_message"])
        return SuccessResponse(200, "Event Created Successfully").get_json()
