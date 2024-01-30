"""
This contains the decorator which will check the role of the
provided token
"""
from flask_jwt_extended import get_jwt
from flask_smorest import abort

from models.response_format import ErrorResponse


def access_level(role):
    """
    For checking the access level from the token
    """

    def check_user(func):
        def wrapper(*args, **kwargs):
            jwt = get_jwt()
            token_role = jwt.get("sub").get("role")
            if token_role in role:
                return func(*args, **kwargs)
            else:
                return abort(
                    403, message=ErrorResponse(403, "Unauthorized Access").get_json()
                )

        return wrapper

    return check_user
