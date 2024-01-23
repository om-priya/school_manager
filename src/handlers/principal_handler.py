"""Principal Handler File"""
import logging
from config.regex_pattern import RegexPatterns
from config.headers_for_output import TableHeaders
from utils.pretty_print import pretty_print
from utils.exception_handler import exception_checker
from utils import validate
from config.sqlite_queries import PrincipalQueries
from config.display_menu import PromptMessage
from helper.helper_function import check_empty_data
from database.database_access import DatabaseAccess

logger = logging.getLogger(__name__)


class PrincipalHandler:
    @staticmethod
    def get_all_active_pid():
        """Fetch All Principal Id who are active"""
        res_data = DatabaseAccess.execute_returning_query(
            PrincipalQueries.FETCH_PRINCIPAL_ID
        )

        return res_data

    @staticmethod
    def get_all_pending_id():
        """Fetch Principal Id who were pending"""
        res_data = DatabaseAccess.execute_returning_query(
            PrincipalQueries.FETCH_PENDING_PRINCIPAL_ID
        )

        return res_data

    @exception_checker
    def approve_principal(self):
        """Approve principal"""
        principal_id = validate.uuid_validator(
            PromptMessage.TAKE_SPECIFIC_ID.format("Principal"),
            RegexPatterns.UUID_PATTERN,
        )

        all_principal_id = self.get_all_active_pid()
        # handling for no principal present
        if len(all_principal_id) == 0:
            pending_id = self.get_all_pending_id()

            # handling for no pending request
            if check_empty_data(
                pending_id, PromptMessage.NOTHING_FOUND.format("request for approval")
            ):
                return

            # checking whether input id is in pending or not
            for p_id in pending_id:
                if p_id[0] == principal_id:
                    break
            else:
                logger.info("Invalid Id's Given")
                print(PromptMessage.NOTHING_FOUND.format("Principal"))
                return
            # saving to db after checking edge cases

            DatabaseAccess.execute_non_returning_query(
                PrincipalQueries.APPROVE_PRINCIPAL, (principal_id,)
            )
        else:
            logger.warning("Can't add more than one principal")
            print(PromptMessage.MULTIPLE_PRINCIPAL_ERROR)
            return

        print(PromptMessage.ADDED_SUCCESSFULLY.format("Principal"))

    @exception_checker
    def get_all_principal(self):
        """Get All principals"""
        res_data = DatabaseAccess.execute_returning_query(
            PrincipalQueries.GET_ALL_PRINCIPAL
        )

        if check_empty_data(res_data, PromptMessage.NOTHING_FOUND.format("Principal")):
            return

        headers = (
            TableHeaders.ID.format("User"),
            TableHeaders.NAME,
            TableHeaders.GENDER,
            TableHeaders.EMAIL,
            TableHeaders.STATUS,
        )
        pretty_print(res_data, headers)

    @exception_checker
    def get_principal_by_id(self):
        """Get Specific principal"""
        principal_id = validate.uuid_validator(
            PromptMessage.TAKE_SPECIFIC_ID.format("Principal"),
            RegexPatterns.UUID_PATTERN,
        )

        res_data = DatabaseAccess.execute_returning_query(
            PrincipalQueries.GET_PRINCIPAL_BY_ID, (principal_id,)
        )

        if check_empty_data(res_data, PromptMessage.NOTHING_FOUND.format("Principal")):
            return

        headers = (
            TableHeaders.ID.format("User"),
            TableHeaders.NAME,
            TableHeaders.GENDER,
            TableHeaders.EMAIL,
            TableHeaders.STATUS,
        )
        pretty_print(res_data, headers)

    @exception_checker
    def update_principal(self):
        """Update principal"""
        # taking input from console
        principal_id = validate.uuid_validator(
            PromptMessage.TAKE_SPECIFIC_ID.format("Principal"),
            RegexPatterns.UUID_PATTERN,
        )
        field_to_update = input(PromptMessage.FIELD_UPDATE).lower()

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

        all_principal_id = self.get_all_active_pid()

        # Checking with assumption only one principal is present
        if principal_id != all_principal_id[0][0]:
            print(PromptMessage.NOTHING_FOUND.format("Principal"))
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
                    PromptMessage.TAKE_INPUT.format("email"),
                    RegexPatterns.EMAIL_PATTERN,
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

        DatabaseAccess.execute_non_returning_query(
            PrincipalQueries.UPDATE_PRINCIPAL.format(table_name, field_to_update),
            (update_value, principal_id),
        )
        print(PromptMessage.SUCCESS_ACTION.format("Updated"))

    @exception_checker
    def delete_principal(self):
        """Delete Principal"""
        principal_id = validate.uuid_validator(
            PromptMessage.TAKE_SPECIFIC_ID.format("Principal"),
            RegexPatterns.UUID_PATTERN,
        )

        all_principal_id = self.get_all_active_pid()

        if principal_id != all_principal_id[0][0]:
            logger.error("No Such Principal With id %s", principal_id)
            print(PromptMessage.NOTHING_FOUND.format("Principal"))
            return

        DatabaseAccess.execute_non_returning_query(
            PrincipalQueries.DELETE_PRINCIPAL, (principal_id,)
        )
        print(PromptMessage.SUCCESS_ACTION.format("Deleted"))
