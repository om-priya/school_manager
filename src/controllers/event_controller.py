import logging
from config.display_menu import PromptMessage
from config.http_status_code import HttpStatusCode
from handlers.event_handler import EventHandler
from flask_smorest import abort
from helper.helper_function import get_user_id_from_jwt, get_request_id
from models.response_format import SuccessResponse, ErrorResponse
from utils.custom_error import ApplicationError

logger = logging.getLogger(__name__)


class EventController:
    def get_all_events(self):
        """Getting all events from handlers anf formatting response"""
        try:
            user_id = get_user_id_from_jwt()
            logger.info(f"{get_request_id()} fetching all events")
            res_data = EventHandler(user_id).read_event()
            return SuccessResponse(
                HttpStatusCode.SUCCESS,
                PromptMessage.LIST_ENTRY.format("Events"),
                res_data,
            ).get_json()
        except ApplicationError as error:
            logger.error(f"{get_request_id()} {error.err_message}")
            return abort(
                error.code,
                message=ErrorResponse(error.code, error.err_message).get_json(),
            )

    def post_create_event(self, event_data):
        user_id = get_user_id_from_jwt()
        logger.info(f"{get_request_id()} creating events call handler")
        EventHandler(user_id).create_event(event_data["event_message"])
        logger.info(
            f"{get_request_id()} event created successfully formatting response"
        )
        return (
            SuccessResponse(
                HttpStatusCode.SUCCESS_CREATED,
                PromptMessage.ADDED_SUCCESSFULLY.format("Event"),
            ).get_json(),
            HttpStatusCode.SUCCESS_CREATED,
        )
