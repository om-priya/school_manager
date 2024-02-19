"""Principal Handler File"""

import logging

# from utils import validate
from config.sqlite_queries import PrincipalQueries
from config.display_menu import PromptMessage
from helper.helper_function import check_empty_data
from database.database_access import DatabaseAccess
from utils.custom_error import DataNotFound, AlreadyPresent
from helper.helper_function import get_request_id

logger = logging.getLogger(__name__)


class PrincipalHandler:
    """
    This class handles the buisness logic for handling
    CRUD on Principal
    """

    @staticmethod
    def get_all_active_pid():
        """Fetch All Principal Id who are active"""
        logger.info(f"{get_request_id()} fetching active principal Id")
        res_data = DatabaseAccess.execute_returning_query(
            PrincipalQueries.FETCH_PRINCIPAL_ID
        )

        return res_data

    @staticmethod
    def get_all_pending_id():
        """Fetch Principal Id who were pending"""
        logger.info(f"{get_request_id()} fetching pending principal Id")
        res_data = DatabaseAccess.execute_returning_query(
            PrincipalQueries.FETCH_PENDING_PRINCIPAL_ID
        )

        return res_data

    def approve_principal(self, principal_id):
        """Approve principal"""
        all_principal_id = self.get_all_active_pid()
        # handling for no principal present
        if len(all_principal_id) == 0:
            pending_id = self.get_all_pending_id()

            # handling for no pending request
            if check_empty_data(
                pending_id, PromptMessage.NOTHING_FOUND.format("request for approval")
            ):
                logger.error(f"{get_request_id()} no pending request to approve")
                raise DataNotFound

            # checking whether input id is in pending or not
            for p_id in pending_id:
                if p_id["user_id"] == principal_id:
                    break
            else:
                logger.info(f"{get_request_id()} Invalid Id's Given")
                raise DataNotFound
            # saving to db after checking edge cases

            DatabaseAccess.execute_non_returning_query(
                PrincipalQueries.APPROVE_PRINCIPAL, (principal_id,)
            )
        else:
            logger.warning(f"{get_request_id()} Can't add more than one principal")
            raise AlreadyPresent

    def get_all_principal(self):
        """Get All principals"""
        logger.info(f"{get_request_id()} fetching all principals")
        res_data = DatabaseAccess.execute_returning_query(
            PrincipalQueries.GET_ALL_PRINCIPAL
        )

        if check_empty_data(res_data, PromptMessage.NOTHING_FOUND.format("Principal")):
            logger.error(f"{get_request_id()} No principal Found")
            raise DataNotFound

        return res_data

    def get_principal_by_id(self, principal_id):
        """Get Specific principal"""
        logger.info(f"{get_request_id()} fetching principal by Id")
        res_data = DatabaseAccess.execute_returning_query(
            PrincipalQueries.GET_PRINCIPAL_BY_ID, (principal_id,)
        )

        if check_empty_data(res_data, PromptMessage.NOTHING_FOUND.format("Principal")):
            logger.error(f"{get_request_id()} no principal by Id {principal_id} found")
            raise DataNotFound

        return res_data

    def update_principal(self, principal_id, principal_updated_details):
        """Update principal"""
        all_principal_id = self.get_all_active_pid()

        # Checking with assumption only one principal is present
        if principal_id != all_principal_id[0]["user_id"]:
            logger.error(f"{get_request_id()} no principal by Id {principal_id} found")
            raise DataNotFound

        name = principal_updated_details["name"]
        gender = principal_updated_details["gender"]
        email = principal_updated_details["email"]
        phone = principal_updated_details["phone"]

        user_table_updated = (name, gender, email, phone, principal_id)
        DatabaseAccess.execute_non_returning_query(
            PrincipalQueries.UPDATE_PRINCIPAL.format("user", user_table_updated),
            (user_table_updated),
        )
        logger.info(f"{get_request_id()} Details updated Successfully")

    def delete_principal(self, principal_id):
        """Delete Principal"""
        all_principal_id = self.get_all_active_pid()

        if principal_id != all_principal_id[0]["user_id"]:
            logger.error(f"{get_request_id()} No Such Principal With id {principal_id}")
            raise DataNotFound

        logger.info(
            f"{get_request_id()} Initiating deleting operations for {principal_id}"
        )
        DatabaseAccess.execute_non_returning_query(
            PrincipalQueries.DELETE_PRINCIPAL, (principal_id,)
        )
        logger.info(
            f"{get_request_id()} Successfull deletion operation for {principal_id}"
        )
