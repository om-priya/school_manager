"""This file contains some helper function which are used for multiple controllers"""

import logging


logger = logging.getLogger(__name__)


def check_empty_data(res_data, prompt_message):
    """This function will check for whether data is there or not"""
    if len(res_data) == 0:
        logger.error(prompt_message)
        return True

    return False
