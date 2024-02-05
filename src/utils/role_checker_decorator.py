"""
This contains the decorator which will check the role of the
provided token
"""

import logging
from flask_smorest import abort

from models.response_format import ErrorResponse
from helper.helper_function import get_user_role_from_jwt, get_request_id

logger = logging.getLogger(__name__)


def access_level(role):
    """
    For checking the access level from the token
    """

    def check_user(func):
        def wrapper(*args, **kwargs):
            token_role = get_user_role_from_jwt()
            if token_role in role:
                logger.info(f"{get_request_id()} has access to the endpoint")
                return func(*args, **kwargs)
            else:
                logger.warn(f"{get_request_id()} has not access to the endpoint")
                return abort(
                    403, message=ErrorResponse(403, "Unauthorized Access").get_json()
                )

        return wrapper

    return check_user
