"""This file contains a decorator which will handle exceptions"""
from functools import wraps
import logging
import sqlite3
from config.display_menu import PromptMessage

logger = logging.getLogger(__name__)


def exception_checker(func):
    """Decorator function to handle exceptions"""

    @wraps(func)
    def exception_handler(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except sqlite3.OperationalError as soe:
            print(f"{PromptMessage.WRONG_QUERY}")
            logger.exception("Something went wrong while executing Query %s", soe)
        except sqlite3.IntegrityError as ige:
            print(f"Integrity Constraint Failed: {ige}")
            logger.exception("Tried to insert duplicate values %s", ige)
        except sqlite3.Error as sqle:
            print(f"Something went wrong with db: {sqle}")
            logger.exception("Something went wrong with db %s", sqle)
        except ValueError as ve:
            print("Wrong Value is provided")
            logger.exception("Wrong Value %s", ve)
        except Exception as e:
            print(f"Something Went Wrong: {e}")
            logger.exception("Something Went Wrong %s", e)

    return exception_handler
