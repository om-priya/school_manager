"""This file contains constants for sqlite queries"""


class DatabaseConfig:
    """This Class contains config for database"""

    CREATE_DB = "CREATE DATABASE IF NOT EXISTS mydb"
    USE_DB = "USE mydb"


class TeacherQueries:
    """This class containst queries for teacher in order of
    CREATE_TABLE, INSERT, READ, UPDATE, DELETE"""

    CREATE_TEACHER_TABLE = """CREATE TABLE IF NOT EXISTS teacher (
        user_id VARCHAR(256) PRIMARY KEY,
        experience INTEGER,
        fav_subject VARCHAR(256)
        )"""
    INSERT_INTO_TEACHER = """INSERT INTO teacher
        (user_id, experience, fav_subject)
        VALUES (%s, %s, %s)"""
    GET_SCHOOL_ID = "SELECT school_id FROM school WHERE school_name = %s"
    GET_APPROVED_TEACHER = """SELECT c.user_id, u.name FROM credential AS c
        INNER JOIN user AS u 
        ON u.user_id = c.user_id 
        WHERE c.role = 'teacher' AND c.status = 'active'"""
    GET_ALL_TEACHER = """SELECT u.user_id, u.name, u.phone, u.email, c.status
        FROM user AS u
        INNER JOIN credential AS c 
        ON u.user_id = c.user_id 
        WHERE c.role = 'teacher' AND c.status = 'active'"""
    APPROVE_TEACHER = """UPDATE credential SET status = 'active'
        WHERE user_id = %s AND status = 'pending' AND role = 'teacher'"""
    GET_TEACHER_BY_ID = """SELECT u.user_id, u.name, u.phone, u.email, c.status
        FROM user AS u
        INNER JOIN credential AS c
        ON u.user_id = c.user_id
        WHERE u.user_id = %s AND c.role = 'teacher' AND c.status = 'active'"""
    FETCH_ACTIVE_TEACHER_ID = """SELECT user_id FROM credential
        WHERE role = 'teacher' AND status = 'active'"""
    FETCH_TEACHER_STATUS = (
        """SELECT status FROM credential WHERE user_id = %s and role = 'teacher'"""
    )
    UPDATE_TEACHER = """UPDATE {} SET {} = %s WHERE user_id = %s"""
    DELETE_TEACHER = """UPDATE credential SET status = 'deactivate'
        WHERE user_id = %s AND role = 'teacher'"""


class PrincipalQueries:
    """This class containst queries for teacher in order of CREATE_TABLE, INSERT, READ, UPDATE"""

    CREATE_PRINCIPAL_TABLE = """CREATE TABLE IF NOT EXISTS principal (
        user_id VARCHAR(256) PRIMARY KEY,
        experience INTEGER
        )"""
    INSERT_INTO_PRINCIPAL = """INSERT INTO principal
        (user_id, experience)
        VALUES (%s, %s)"""
    APPROVE_PRINCIPAL = """UPDATE credential SET status = 'active'
        WHERE user_id = %s AND status = 'pending' AND role = 'principal'"""
    GET_ALL_PRINCIPAL = """SELECT u.user_id, u.name, u.gender, u.email, c.status
        FROM user AS u
        INNER JOIN credential AS c
        ON c.user_id = u.user_id
        WHERE c.role = 'principal' AND c.status = 'active'"""
    GET_PRINCIPAL_BY_ID = """SELECT u.user_id, u.name, u.gender, u.email, c.status
        FROM user AS u
        INNER JOIN credential AS c
        ON c.user_id = u.user_id
        WHERE c.user_id = %s AND c.role = 'principal'"""
    FETCH_PRINCIPAL_ID = """SELECT user_id FROM credential
        WHERE role = 'principal' AND status = 'active'"""
    FETCH_PENDING_PRINCIPAL_ID = """SELECT user_id FROM credential
        WHERE role = 'principal' AND status = 'pending'"""
    UPDATE_PRINCIPAL = """UPDATE {} SET {} = %s WHERE user_id = %s"""
    DELETE_PRINCIPAL = """UPDATE credential SET status = 'deactivate'
        WHERE user_id = %s AND role = 'principal'"""
    READ_FEEDBACKS_PRINCIPAL = """SELECT feedback_id, message, created_date FROM feedbacks
        WHERE raised_by = %s"""


class StaffQueries:
    """This class containt queries for staff members in order of
    CREATE_TABLE, INSERT, READ, UPDATE"""

    INSERT_INTO_STAFF_MEMBER = """INSERT INTO staff_member
        (user_id, expertise, name, gender, address, phone, status, school_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    VIEW_ALL_STAFF = """SELECT * FROM staff_member WHERE status = 'active'
    AND school_id = (SELECT school_id FROM mapping AS m WHERE m.user_id = %s)"""
    GET_SCHOOL_ID_STAFF = """SELECT school_id FROM mapping AS m WHERE m.user_id = %s"""
    UPDATE_STAFF = """UPDATE staff_member
                    SET {} = %s
                    WHERE user_id = %s AND status = 'active'"""
    DELETE_STAFF = """UPDATE staff_member
                    SET status = 'deactivate'
                    WHERE user_id = %s AND status = 'active'"""
    FETCH_STAFF_STATUS = """SELECT status FROM staff_member WHERE user_id = %s"""


class UserQueries:
    """This class contain queries for users which are common for all"""

    FETCH_FROM_CREDENTIALS = """SELECT user_id, role, status
        FROM credential
        WHERE username = %s AND password = %s"""
    FETCH_LEAVE_STATUS = (
        """SELECT leave_date, no_of_days, status FROM leaves WHERE user_id = %s"""
    )
    GET_PENDING_LEAVES = """SELECT * FROM leaves WHERE status = 'pending'"""
    APPROVE_LEAVE = """UPDATE leaves SET status = 'approved'
        WHERE leave_id = %s AND status = 'pending'"""
    GET_ALL_ISSUES = """SELECT * FROM issue"""
    GET_SALARY_HISTORY = """SELECT salary_id, year, month, amount, pay_date
        FROM salary
        WHERE user_id = %s
        ORDER BY year DESC, month ASC"""
    READ_NOTICE = """SELECT notice_id, notice_message FROM notice"""
    READ_FEEDBACKS = """SELECT feedback_id, message, created_date
        FROM feedbacks
        WHERE given_to = %s"""
    FETCH_SUPER_ADMIN = """SELECT * FROM credential
        WHERE role = 'superadmin'"""
    CHECK_USER_EXIST = """SELECT *
        FROM credential 
        WHERE username = %s AND password = %s AND user_id = %s AND status = 'active'"""
    CHANGE_PASSWORD_QUERY = """UPDATE credential SET password = %s WHERE user_id = %s"""
    FETCH_FROM_TOKEN = """SELECT * FROM block_token WHERE token_id = %s"""


class CreateTable:
    """Queries to create tables"""

    CREATE_CREDENTIALS_TABLE = """CREATE TABLE IF NOT EXISTS credential (
    username VARCHAR(256) UNIQUE,
    password VARCHAR(100),
    user_id VARCHAR(256) PRIMARY KEY,
    role VARCHAR(256),
    status VARCHAR(256)
    )"""
    CREATE_USERS_TABLE = """CREATE TABLE IF NOT EXISTS user (
        user_id VARCHAR(256) PRIMARY KEY,
        name VARCHAR(256),
        gender VARCHAR(256),
        email VARCHAR(256) UNIQUE,
        phone VARCHAR(256) UNIQUE
    )"""
    CREATE_SCHOOL_TABLE = """CREATE TABLE IF NOT EXISTS school (
        school_id VARCHAR(256) PRIMARY KEY,
        school_name VARCHAR(256),
        location VARCHAR(256),
        email VARCHAR(256) UNIQUE,
        contact VARCHAR(256) UNIQUE
    )"""
    CREATE_TEACHER_TABLE = """CREATE TABLE IF NOT EXISTS teacher (
        user_id VARCHAR(256) PRIMARY KEY,
        experience INTEGER,
        fav_subject VARCHAR(256)
    )"""
    CREATE_LEAVE_TABLE = """CREATE TABLE IF NOT EXISTS leaves (
        leave_id VARCHAR(256) PRIMARY KEY,
        leave_date VARCHAR(256),
        no_of_days INTEGER,
        user_id VARCHAR(256),
        status VARCHAR(256)
    )"""
    CREATE_NOTICE_TABLE = """CREATE TABLE IF NOT EXISTS notice (
        notice_id VARCHAR(256) PRIMARY KEY,
        created_by VARCHAR(256),
        notice_message VARCHAR(256),
        created_date VARCHAR(256)
    )"""
    CREATE_ISSUES_TABLE = """CREATE TABLE IF NOT EXISTS issue (
        issue_id VARCHAR(256) PRIMARY KEY,
        issue_message VARCHAR(256),
        raised_by VARCHAR(256)
    )"""
    CREATE_FEEDBACKS_TABLE = """CREATE TABLE IF NOT EXISTS feedbacks (
        feedback_id VARCHAR(256) PRIMARY KEY,
        message VARCHAR(256),
        created_date VARCHAR(256),
        given_to VARCHAR(256),
        raised_by VARCHAR(256)
    )"""
    CREATE_SALARY_TABLE = """CREATE TABLE IF NOT EXISTS salary (
        salary_id VARCHAR(256) PRIMARY KEY,
        user_id VARCHAR(256),
        amount INTEGER,
        year INTEGER,
        month INTEGER,
        pay_date VARCHAR(256),
        FOREIGN KEY (user_id) REFERENCES user(user_id)
    )"""
    CREATE_USER_SCHOOL_MAP_TABLE = """CREATE TABLE IF NOT EXISTS mapping (
        user_id VARCHAR(256) PRIMARY KEY,
        school_id VARCHAR(256)
    )"""
    CREATE_PRINCIPAL_TABLE = """CREATE TABLE IF NOT EXISTS principal (
        user_id VARCHAR(256) PRIMARY KEY,
        experience INTEGER
    )"""
    CREATE_STAFF_MEMBER_TABLE = """CREATE TABLE IF NOT EXISTS staff_member (
        user_id VARCHAR(256) PRIMARY KEY,
        expertise VARCHAR(256),
        name VARCHAR(256),
        gender VARCHAR(256),
        address VARCHAR(256),
        phone VARCHAR(256) UNIQUE,
        status VARCHAR(256),
        school_id VARCHAR(256)
    )"""
    CREATE_TOKEN_TABLE = """CREATE TABLE IF NOT EXISTS block_token (
        token_id VARCHAR(256) PRIMARY KEY
    )"""
    INSERT_INTO_TOKEN = """INSERT INTO block_token
        (token_id)
        VALUES (%s)"""
    INSERT_INTO_CREDENTIAL = """INSERT INTO credential
    (username, password, user_id, role, status) 
    VALUES (%s, %s, %s, %s, %s)"""
    INSERT_INTO_USER = """INSERT INTO user
        (user_id, name, gender, email, phone)
        VALUES (%s, %s, %s, %s, %s)"""
    INSERT_INTO_MAPPING = """INSERT INTO mapping
        (user_id, school_id)
        VALUES (%s, %s)"""
    INSERT_INTO_SCHOOL = """INSERT INTO school
        (school_id, school_name, location, email, contact)
        VALUES (%s, %s, %s, %s, %s)"""
    INSERT_INTO_LEAVES = """INSERT INTO leaves
        (leave_id, leave_date, no_of_days, user_id, status)
        VALUES (%s, %s, %s, %s, %s)"""
    INSERT_INTO_NOTICE = """INSERT INTO notice
        (notice_id, created_by, notice_message, created_date)
        VALUES (%s, %s, %s, %s)"""
    INSERT_INTO_ISSUE = """INSERT INTO issue
        (issue_id, issue_VARCHAR(256), raised_by)
        VALUES (%s, %s, %s)"""
    INSERT_INTO_FEEDBACKS = """INSERT INTO feedbacks
        (feedback_id, message, created_date, given_to, raised_by) 
        VALUES (%s, %s, %s, %s, %s)"""
    INSERT_INTO_SALARY = """INSERT INTO salary
        (salary_id, user_id, amount, year, month, pay_date)
        VALUES (%s, %s, %s, %s, %s, %s)"""
    INSERT_INTO_ATTENDANCE = """INSERT INTO attendance
        (attendance_id, user_id, time_in, time_out, attendance_date)
        VALUES (%s, %s, %s, %s, %s)"""
