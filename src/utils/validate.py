"""This module is responsible for validating input fields"""

import re
from datetime import datetime
import maskpass
import logging
from config.regex_pattern import RegexPatterns
from config.display_menu import PromptMessage

logger = logging.getLogger(__name__)


def validator(pattern, input_data):
    """
    General validator function that returns True if the input data matches the specified pattern,
    otherwise prints an error message and returns False.

    Parameters:
    - pattern (str): The regular expression pattern to match.
    - input_data (str): The input data to validate.

    Returns:
    bool: True if the input data matches the pattern, False otherwise.
    """
    x = re.fullmatch(pattern, input_data)
    if x is None:
        print(PromptMessage.INVALID_INPUT.format("pattern doesn't match"))
        return False
    return True


def pattern_validator(prompt, pattern):
    """
    Generic function to validate data using a specified pattern.

    Parameters:
    - prompt (str): The prompt to display when taking user input.
    - pattern (str): The regular expression pattern to match.

    Returns:
    str: The validated input data.
    """
    input_data = ""
    validated = False
    while validated is False:
        input_data = input(prompt).lower()
        validated = validator(pattern, input_data)
    return input_data


def uuid_validator(prompt, pattern):
    """
    Function to validate UUID.

    Parameters:
    - prompt (str): The prompt to display when taking user input.
    - pattern (str): The regular expression pattern to match.

    Returns:
    str: The validated UUID.
    """
    uuid = ""
    validated = False
    while validated is False:
        uuid = input(prompt)
        validated = validator(pattern, uuid)
    return uuid


def password_validator():
    """
    Function to validate a strong password.

    Returns:
    str: The validated password.
    """
    password = ""
    validated = False
    while validated is False:
        password = maskpass.advpass()
        validated = validator(
            RegexPatterns.PASSWORD_PATTERN,
            password,
        )
    return password


def validate_date(prompt) -> None:
    """
    Function to validate a date.

    Parameters:
    - prompt (str): The prompt to display when taking user input.

    Returns:
    datetime.date: The validated date.
    """
    while True:
        date_str = input(prompt)
        try:
            start_date = datetime.strptime(date_str, "%d-%m-%Y").date()
            if start_date > datetime.now().date():
                return start_date
            elif start_date <= datetime.now().date():
                print(PromptMessage.INVALID_INPUT.format("For Date"))
        except ValueError:
            logger.exception(ValueError)
            print(PromptMessage.INVALID_INPUT.format("For Date"))
