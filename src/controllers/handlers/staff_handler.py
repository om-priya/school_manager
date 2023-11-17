"""Staff Handler File"""
import shortuuid
from src.config.regex_pattern import RegexPatterns
from src.config.sqlite_queries import StaffQueries
from src.config.headers_for_output import TableHeaders
from src.config.display_menu import PromptMessage
from src.database import database_access as DAO
from src.utils.pretty_print import pretty_print
from src.utils.exception_handler import exception_checker
from src.utils import validate


def fetch_staff_status(staff_id):
    """This function will fetch the staff id which will be used for checks"""
    res_data = DAO.execute_returning_query(StaffQueries.FETCH_STAFF_STATUS, (staff_id,))
    return res_data


def check_staff(staff_id):
    """This function return true or false"""
    staff_status = fetch_staff_status(staff_id)

    if len(staff_status) != 0 and staff_status[0][0] == "active":
        return True

    return False


@exception_checker
def view_staff(user_id):
    """View Staff Members"""
    res_data = DAO.execute_returning_query(StaffQueries.VIEW_ALL_STAFF, (user_id,))

    # for no staff members
    if len(res_data) == 0:
        print(PromptMessage.NOTHING_FOUND.format("Staff"))
        return

    headers = (
        TableHeaders.ID.format("Staff"),
        TableHeaders.EXPERTISE,
        TableHeaders.NAME,
        TableHeaders.PHONE,
        TableHeaders.ADDRESS,
        TableHeaders.GENDER,
        TableHeaders.STATUS,
        TableHeaders.ID.format("School"),
    )

    pretty_print(res_data, headers=headers)


@exception_checker
def create_staff(user_id):
    """Create Staff Members"""
    # getting info to save it in db
    staff_id = shortuuid.ShortUUID().random(length=6)
    name = validate.pattern_validator(
        PromptMessage.TAKE_INPUT.format("Name"), RegexPatterns.NAME_PATTERN
    )
    expertise = validate.pattern_validator(
        PromptMessage.TAKE_INPUT.format("Expertise"), RegexPatterns.NAME_PATTERN
    )
    phone = validate.pattern_validator(
        PromptMessage.TAKE_INPUT.format("Phone Number"), RegexPatterns.PHONE_PATTERN
    )
    address = validate.pattern_validator(
        PromptMessage.TAKE_INPUT.format("Address"), RegexPatterns.NAME_PATTERN
    )
    gender = validate.pattern_validator(
        PromptMessage.TAKE_INPUT.format("Gender (M/F)"), RegexPatterns.GENDER_PATTERN
    )
    status = "active"

    # fetching school id of super admin who is logged in
    school_id = DAO.execute_returning_query(
        StaffQueries.GET_SCHOOL_ID_STAFF, (user_id,)
    )[0][0]

    # inserting info to db
    DAO.execute_non_returning_query(
        StaffQueries.INSERT_INTO_STAFF_MEMBER,
        (staff_id, expertise, name, gender, address, phone, status, school_id),
    )

    print(PromptMessage.ADDED_SUCCESSFULLY.format("Staff"))


@exception_checker
def update_staff():
    """Update staff"""
    staff_id = validate.uuid_validator(
        PromptMessage.TAKE_SPECIFIC_ID.format("Staff"), RegexPatterns.UUID_PATTERN
    )

    if not check_staff(staff_id):
        print(PromptMessage.NOTHING_FOUND.format("Staff"))
        return

    field_to_update = input(PromptMessage.FIELD_UPDATE).lower()
    options = (
        TableHeaders.NAME.lower(),
        TableHeaders.PHONE.lower(),
        TableHeaders.GENDER.lower(),
    )

    # if wrong field is provided
    if field_to_update not in options:
        print(PromptMessage.INVALID_INPUT)
        return

    # taking updated value with input validation
    if field_to_update == "gender":
        updated_value = validate.pattern_validator(
            PromptMessage.TAKE_INPUT.format("Gender (M/F)"),
            RegexPatterns.GENDER_PATTERN,
        )
    elif field_to_update == "phone":
        updated_value = validate.pattern_validator(
            PromptMessage.TAKE_INPUT.format("Phone Number"), RegexPatterns.PHONE_PATTERN
        )
    else:
        updated_value = validate.pattern_validator(
            PromptMessage.TAKE_INPUT.format("Name"), RegexPatterns.NAME_PATTERN
        )

    # updating value to db
    DAO.execute_non_returning_query(
        StaffQueries.UPDATE_STAFF.format(field_to_update), (updated_value, staff_id)
    )
    print(PromptMessage.SUCCESS_ACTION.format("Updated"))


@exception_checker
def delete_staff():
    """Delete staff"""
    staff_id = validate.uuid_validator(
        PromptMessage.TAKE_SPECIFIC_ID.format("Staff"), RegexPatterns.UUID_PATTERN
    )

    if not check_staff(staff_id):
        print(PromptMessage.NOTHING_FOUND.format("Staff"))
        return

    DAO.execute_non_returning_query(StaffQueries.DELETE_STAFF, (staff_id,))
    print(PromptMessage.SUCCESS_ACTION.format("Deleted"))
