"""Principal Handler File"""
import logging
from src.config.regex_pattern import RegexPatterns
from src.config.headers_for_output import TableHeaders
from src.utils.pretty_print import pretty_print
from src.utils import validate
from src.config.sqlite_queries import PrincipalQueries
from src.config.display_menu import PromptMessage
from src.database import database_access as DAO

logger = logging.getLogger(__name__)


def get_all_active_pid():
    """Fetch All Principal Id who are active"""
    res_data = DAO.execute_returning_query(PrincipalQueries.FETCH_PRINCIPAL_ID)

    return res_data


def get_all_pending_id():
    """Fetch Principal Id who were pending"""
    res_data = DAO.execute_returning_query(PrincipalQueries.FETCH_PENDING_PRINCIPAL_ID)

    return res_data


def approve_principal():
    """Approve principal"""
    principal_id = validate.uuid_validator(
        PromptMessage.TAKE_SPECIFIC_ID.format("Principal"), RegexPatterns.UUID_PATTERN
    )

    all_principal_id = get_all_active_pid()

    # handling for no principal present
    if len(all_principal_id) == 0:
        pending_id = get_all_pending_id()

        # handling for no pending request
        if len(pending_id) == 0:
            logger.error("No request for approval")
            print(PromptMessage.NOTHING_FOUND.format("request for approval"))
            return

        # checking whether input id is in pending or not
        for p_id in pending_id[0]:
            if p_id == principal_id:
                break
            else:
                logger.info("Invalid Id's Given")
                print(PromptMessage.NOTHING_FOUND.format("Principal"))
                return
        # saving to db after checking edge cases

        DAO.execute_non_returning_query(
            PrincipalQueries.APPROVE_PRINCIPAL, (principal_id,)
        )
    else:
        logger.warning("Can't add more than one principal")
        print(PromptMessage.MULTIPLE_PRINCIPAL_ERROR)
        return

    print(PromptMessage.ADDED_SUCCESSFULLY.format("Principal"))


def get_all_principal():
    """Get All principals"""
    res_data = DAO.execute_returning_query(PrincipalQueries.GET_ALL_PRINCIPAL)

    if len(res_data) == 0:
        logger.error("No Principal Found")
        print(PromptMessage.NOTHING_FOUND.format("Principal"))
        return

    headers = ["User_id", "name", "gender", "email", "status"]
    headers = (
        TableHeaders.ID.format("User"),
        TableHeaders.NAME,
        TableHeaders.GENDER,
        TableHeaders.EMAIL,
        TableHeaders.STATUS,
    )
    pretty_print(res_data, headers)


def get_principal_by_id():
    """Get Specific principal"""
    principal_id = validate.uuid_validator(
        PromptMessage.TAKE_SPECIFIC_ID.format("Principal"), RegexPatterns.UUID_PATTERN
    )

    res_data = DAO.execute_returning_query(
        PrincipalQueries.GET_PRINCIPAL_BY_ID, (principal_id,)
    )

    if len(res_data) == 0:
        logger.error("No Principal Found")
        print(PromptMessage.NOTHING_FOUND.format("Principal"))
        return

    headers = (
        TableHeaders.ID.format("User"),
        TableHeaders.NAME,
        TableHeaders.GENDER,
        TableHeaders.EMAIL,
        TableHeaders.STATUS,
    )
    pretty_print(res_data, headers)


def update_principal():
    """Update principal"""
    # taking input from console
    principal_id = validate.uuid_validator(
        PromptMessage.TAKE_SPECIFIC_ID.format("Principal"), RegexPatterns.UUID_PATTERN
    )
    field_to_update = input(PromptMessage.FIELD_UPDATE).lower()

    all_principal_id = get_all_active_pid()

    # Checking with assumption only one principal is present
    if principal_id != all_principal_id[0][0]:
        print(PromptMessage.NOTHING_FOUND.format("Principal"))
        return

    options = (
        TableHeaders.NAME.lower(),
        TableHeaders.GENDER.lower(),
        TableHeaders.EMAIL.lower(),
        TableHeaders.PHONE.lower(),
        TableHeaders.EXPERIENCE.lower(),
    )

    # checking field to update
    if field_to_update not in options:
        logger.info("No Such Field is present")
        print(PromptMessage.NOTHING_FOUND.format("Field"))
        return

    # getting table name
    if field_to_update in options[:4]:
        table_name = "user"
    else:
        table_name = "principal"

    # validating and saving to db
    match field_to_update:
        case "name":
            update_value = validate.pattern_validator(
                PromptMessage.TAKE_INPUT.format("Name"), RegexPatterns.NAME_PATTERN
            )
        case "gender":
            update_value = validate.pattern_validator(
                PromptMessage.TAKE_INPUT.format("Gender (M/F)"),
                RegexPatterns.GENDER_PATTERN,
            )
        case "email":
            update_value = validate.pattern_validator(
                PromptMessage.TAKE_INPUT.format("email"), RegexPatterns.EMAIL_PATTERN
            )
        case "phone":
            update_value = validate.pattern_validator(
                PromptMessage.TAKE_INPUT.format("Phone Number"),
                RegexPatterns.PHONE_PATTERN,
            )
        case "experience":
            update_value = validate.pattern_validator(
                PromptMessage.TAKE_INPUT.format("Experience in Year"),
                RegexPatterns.EXPERIENCE_PATTERN,
            )

    DAO.execute_non_returning_query(
        PrincipalQueries.UPDATE_PRINCIPAL.format(table_name, field_to_update),
        (update_value, principal_id),
    )


def delete_principal():
    """Delete principal of principal"""
    principal_id = validate.uuid_validator(
        PromptMessage.TAKE_SPECIFIC_ID.format("Principal"), RegexPatterns.UUID_PATTERN
    )

    all_principal_id = get_all_active_pid()

    if principal_id != all_principal_id[0][0]:
        logger.error("No Such Principal With id %s", principal_id)
        print(PromptMessage.NOTHING_FOUND.format("Principal"))
        return

    DAO.execute_non_returning_query(PrincipalQueries.DELETE_PRINCIPAL, (principal_id,))
