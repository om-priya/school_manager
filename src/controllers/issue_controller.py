import logging

from handlers.issue_handler import IssueHandler
from utils.custom_error import ApplicationError
from models.response_format import SuccessResponse, ErrorResponse
from helper.helper_function import get_user_id_from_jwt
from config.display_menu import PromptMessage
from config.http_status_code import HttpStatusCode
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
                HttpStatusCode.SUCCESS,
                PromptMessage.LIST_ENTRY.format("Issues raised by teachers"),
                res_data,
            ).get_json()
        except ApplicationError as error:
            logger.error(f"{get_request_id()} {error.err_message}")
            return ErrorResponse(error.code, error.err_message).get_json(), error.code

    def create_issue_controller(self, issue_mssg):
        user_id = get_user_id_from_jwt()

        logger.info(f"{get_request_id()} calling handler for creating issues")
        IssueHandler(user_id).raise_issue(issue_mssg["issue_message"])
        logger.info(
            f"{get_request_id()} formatting response after successfull creation of issue"
        )
        return (
            SuccessResponse(
                HttpStatusCode.SUCCESS_CREATED,
                PromptMessage.ADDED_SUCCESSFULLY.format("Issue"),
            ).get_json(),
            HttpStatusCode.SUCCESS_CREATED,
        )
