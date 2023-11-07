"""This file contains a decorator which will handle exceptions"""
from functools import wraps
import logging
import sqlite3

logger = logging.getLogger(__name__)


def exception_checker(func):
    """This is a decorator function to handle exception"""

    @wraps(func)
    def exception_handler(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except sqlite3.OperationalError as soe:
            print(f"Something went wrong while executing the query: {soe}")
        except sqlite3.IntegrityError as ige:
            print(f"Integrity Constraint Failed: {ige}")
        except sqlite3.Error as sqle:
            print(f"Something went wrong with db: {sqle}")
            logger.exception("Something went wrong with db %s", sqle)
        except Exception as e:
            logger.exception("Something Went Wrong %s", e)
            print(f"Something Went Wrong: {e}")

    return exception_handler
