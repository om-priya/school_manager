"""For saving super Admin to Db"""
import os
import shortuuid
from dotenv import load_dotenv
from src.database import database_access as DAO
from src.config.sqlite_queries import CreateTable
from src.utils.hash_password import hash_password

load_dotenv()


def create_super_admin():
    """Create super Admin to db if super admin doesn't exists"""
    user_id = "S" + shortuuid.ShortUUID().random(length=6)
    school_id = shortuuid.ShortUUID().random(length=6)
    name = os.getenv("NAME")
    gender = os.getenv("GENDER")
    email = os.getenv("EMAIL")
    phone = os.getenv("PHONE")
    role = os.getenv("ROLE")
    status = os.getenv("STATUS")
    user_name = os.getenv("USER_NAME")
    password = os.getenv("PASSWORD")
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
    DAO.execute_non_returning_query(CreateTable.INSERT_INTO_CREDENTIAL, cred_tuple)
    DAO.execute_non_returning_query(CreateTable.INSERT_INTO_MAPPING, map_tuple)
    DAO.execute_non_returning_query(CreateTable.INSERT_INTO_USER, user_tuple)
    DAO.execute_non_returning_query(CreateTable.INSERT_INTO_SCHOOL, school_tuple)
