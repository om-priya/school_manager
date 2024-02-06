import logging
from config.display_menu import PromptMessage
from handlers.event_handler import EventHandler
from flask_smorest import abort
from helper.helper_function import get_user_id_from_jwt, get_request_id
from models.response_format import SuccessResponse, ErrorResponse
from utils.custom_error import DataNotFound

logger = logging.getLogger(__name__)


class EventController:
    def get_all_events(self):
        try:
            user_id = get_user_id_from_jwt()
            logger.info(f"{get_request_id()} fetching all events")
            res_data = EventHandler(user_id).read_event()
            return SuccessResponse(
                200, PromptMessage.LIST_ENTRY.format("Events"), res_data
            ).get_json()
        except DataNotFound:
            logger.error(
                f"{get_request_id()} No events founds formatting error response"
            )
            return abort(
                404,
                message=ErrorResponse(
                    404, PromptMessage.NOTHING_FOUND.format("Events")
                ).get_json(),
            )

    def post_create_event(self, event_data):
        user_id = get_user_id_from_jwt()
        logger.info(f"{get_request_id()} creating events call handler")
        EventHandler(user_id).create_event(event_data["event_message"])
        logger.info(
            f"{get_request_id()} event created successfully formatting response"
        )
        return SuccessResponse(
            201, PromptMessage.ADDED_SUCCESSFULLY.format("Event")
        ).get_json()
