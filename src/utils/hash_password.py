""" To hash the password using hashlib """
import hashlib


def hash_password(password):
    """This function is responsible for hashing password"""
    hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return hashed_password
