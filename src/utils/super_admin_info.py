"""For saving super Admin to Db"""
import os
import shortuuid
from dotenv import load_dotenv
from database.db_connector import DatabaseConnection
from config.sqlite_queries import CreateTable
from utils.hash_password import hash_password

load_dotenv()


def create_super_admin():
    """
    Create a super admin in the database if one doesn't already exist.

    Retrieves necessary information from environment variables and generates unique identifiers.
    Hashes the password, then saves the super admin information to the database.

    Parameters:
    None

    Returns:
    None
    """
    user_id = "S" + shortuuid.ShortUUID().random(length=6)
    school_id = shortuuid.ShortUUID().random(length=6)
    name = os.getenv("NAME")
    gender = os.getenv("GENDER")
    email = os.getenv("EMAIL")
    phone = os.getenv("PHONE")
    role = os.getenv("ROLE")
    status = os.getenv("STATUS")
    user_name = os.getenv("USER_NAME")
    password = os.getenv("SUPER_PASSWORD")
    hashed_password = hash_password(password)
    school_name = os.getenv("SCHOOL_NAME")
    school_location = os.getenv("SCHOOL_LOCATION")
    school_email = os.getenv("SCHOOL_EMAIL")
    school_contact = os.getenv("SCHOOL_CONTACT")

    # save these info to db

    # save super admin query
    # Tuples for storing info
    cred_tuple = (user_name, hashed_password, user_id, role, status)
    map_tuple = (user_id, school_id)
    user_tuple = (user_id, name, gender, email, phone)
    school_tuple = (
        school_id,
        school_name,
        school_location,
        school_email,
        school_contact,
    )

    # Execute query
    with DatabaseConnection() as connection:
        cursor = connection.cursor()
        cursor.execute(CreateTable.INSERT_INTO_CREDENTIAL, cred_tuple)
        cursor.execute(CreateTable.INSERT_INTO_MAPPING, map_tuple)
        cursor.execute(CreateTable.INSERT_INTO_USER, user_tuple)
        cursor.execute(CreateTable.INSERT_INTO_SCHOOL, school_tuple)
