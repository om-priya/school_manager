from flask_jwt_extended import get_jwt
from flask_smorest import abort

from models.response_format import ErrorResponse


def access_level(role):
    def check_user(*args, **kwargs):
        def wrapper(func):
            jwt = get_jwt()
            token_role = jwt.get("sub").get("role")
            if token_role in role:
                return func()
            else:
                return abort(403, message=ErrorResponse(403, "Unauthorized Access").get_json())

        return wrapper

    return check_user
