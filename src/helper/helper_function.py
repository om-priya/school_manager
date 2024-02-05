"""This file contains some helper function which are used for multiple controllers"""

import logging
from flask_jwt_extended import get_jwt
from flask import request

logger = logging.getLogger(__name__)


def get_request_id():
    return request.environ.get("X-Request-Id")


def check_empty_data(res_data, prompt_message):
    """This function will check for whether data is there or not"""
    if len(res_data) == 0:
        logger.error(f"{get_request_id} {prompt_message}")
        return True

    return False


def get_user_id_from_jwt():
    jwt = get_jwt()
    user_id = jwt.get("sub").get("user_id")
    return user_id


def get_user_role_from_jwt():
    jwt = get_jwt()
    role = jwt.get("sub").get("role")
    return role

def get_token_id_from_jwt():
    jwt = get_jwt()
    token_id = jwt.get("token_id")
    return token_id
