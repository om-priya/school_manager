""" To hash the password using hashlib """
import hashlib


def hash_password(password):
    """
    Hashes the provided password using SHA-256 with a unique salt.

    Parameters:
    - password (str): The password to be hashed.

    Returns:
    str: The hashed password.
    """
    hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return hashed_password
