from flask_smorest import abort
from handlers.issue_handler import IssueHandler
from utils.custom_error import DataNotFound
from models.response_format import SuccessResponse, ErrorResponse
from helper.helper_function import get_user_id_from_jwt

class IssueController:
    def get_all_issues(self):
        try:
            user_id = get_user_id_from_jwt()

            res_data = IssueHandler(user_id).view_issue()

            return SuccessResponse(
                200, "Here's the Issues raised by teachers", res_data
            ).get_json()
        except DataNotFound:
            return abort(404, message=ErrorResponse(404, "No Such Issues Found"))

    def create_issue_controller(self, issue_mssg):
        user_id = get_user_id_from_jwt()

        IssueHandler(user_id).raise_issue(issue_mssg["issue_message"])
        return SuccessResponse(201, "Issue Raised SuccessFully").get_json()
