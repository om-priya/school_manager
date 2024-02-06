import logging

from flask_smorest import abort
from handlers.issue_handler import IssueHandler
from utils.custom_error import DataNotFound
from models.response_format import SuccessResponse, ErrorResponse
from helper.helper_function import get_user_id_from_jwt
from config.display_menu import PromptMessage
from helper.helper_function import get_request_id

logger = logging.getLogger(__name__)


class IssueController:
    def get_all_issues(self):
        try:
            user_id = get_user_id_from_jwt()
            logger.info(f"{get_request_id()} calling handler for fetching issues")
            res_data = IssueHandler(user_id).view_issue()

            logger.info(f"{get_request_id()} formatting response for issues fetched")
            return SuccessResponse(
                200,
                PromptMessage.LIST_ENTRY.format("Issues raised by teachers"),
                res_data,
            ).get_json()
        except DataNotFound:
            logger.error(f"{get_request_id()} formatting response for no issues found")
            return abort(
                404,
                message=ErrorResponse(404, PromptMessage.NOTHING_FOUND.format("Issue")),
            )

    def create_issue_controller(self, issue_mssg):
        user_id = get_user_id_from_jwt()

        logger.info(f"{get_request_id()} calling handler for creating issues")
        IssueHandler(user_id).raise_issue(issue_mssg["issue_message"])
        logger.info(
            f"{get_request_id()} formatting response after successfull creation of iisue"
        )
        return SuccessResponse(
            201, PromptMessage.ADDED_SUCCESSFULLY.format("Issue")
        ).get_json()
