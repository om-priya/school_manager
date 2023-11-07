"""This module is responsible for validating input fields"""

import re
import maskpass
from src.config.regex_pattern import RegexPatterns

from src.config.display_menu import PromptMessage


def validator(pattern, input_data):
    """General Validator which return either True or False"""
    x = re.fullmatch(pattern, input_data)
    if x is None:
        print(PromptMessage.INVALID_INPUT.format("pattern doesn't match"))
        return False
    return True


def pattern_validator(prompt, pattern):
    """Generic Function to validate data"""
    input_data = ""
    validated = False
    while validated is False:
        input_data = input(prompt).lower()
        validated = validator(pattern, input_data)
    return input_data


def password_validator():
    """Strong Password"""
    password = ""
    validated = False
    while validated is False:
        password = maskpass.advpass()
        validated = validator(
            RegexPatterns.PASSWORD_PATTERN,
            password,
        )
    return password
