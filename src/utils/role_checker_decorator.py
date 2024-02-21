"""
This contains the decorator which will check the role of the
provided token
"""

import logging

from models.response_format import ErrorResponse
from helper.helper_function import (
    get_user_role_from_jwt,
    get_request_id,
    get_token_id_from_jwt,
)
from config.sqlite_queries import UserQueries
from config.http_status_code import HttpStatusCode
from database.database_access import DatabaseAccess

logger = logging.getLogger(__name__)


def access_level(role):
    """
    For checking the access level from the token
    """

    def check_user(func):
        def wrapper(*args, **kwargs):
            token_role = get_user_role_from_jwt()
            token_id = get_token_id_from_jwt()
            res_data = DatabaseAccess.execute_returning_query(
                UserQueries.FETCH_FROM_TOKEN, (token_id,)
            )
            if token_role in role and not res_data:
                logger.info(f"{get_request_id()} has access to the endpoint")
                return func(*args, **kwargs)
            elif token_role not in role:
                logger.warn(f"{get_request_id()} has not access to the endpoint")
                return (
                    ErrorResponse(
                        HttpStatusCode.FORBIDDEN, "Unauthorized Access"
                    ).get_json(),
                    HttpStatusCode.FORBIDDEN,
                )

            elif res_data:
                logger.critical(
                    f"{get_request_id()} has access the endpoint with blocked token"
                )
                return (
                    ErrorResponse(
                        HttpStatusCode.FORBIDDEN, "Token is Blocked"
                    ).get_json(),
                    HttpStatusCode.FORBIDDEN,
                )

        return wrapper

    return check_user
