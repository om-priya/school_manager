"""
Response Format class fro returning the generic response format
"""


class ErrorResponse:
    """
    Represents an error response with status code and message.

    Attributes:
        success (bool): A class attribute indicating whether the \
            response is successful (default is False).
        err_status_code (int): The HTTP status code associated with the error.
        err_message (str): A human-readable message describing the error.

    Methods:
        get_json(): Returns a dictionary representing the error response in JSON format.

    Example:
        error_response = ErrorResponse(status_code=404, message="Resource not found")
        error_data = error_response.get_json()
    """

    success = False

    def __init__(self, status_code, message):
        self.err_status_code = status_code
        self.err_message = message

    def get_json(self):
        """
        Returns a dictionary representing the error response in JSON format.

        Returns:
            dict: A dictionary with keys 'success', 'err_status_code', and 'err_message'.
        """
        return {
            "success": ErrorResponse.success,
            "err_status_code": self.err_status_code,
            "err_message": self.err_message,
        }


class SuccessResponse:
    """
    Represents a successful response with status code, message, and optional data.

    Attributes:
    success (bool): A class attribute indicating whether the response is \
        successful (default is True).
    status_code (int): The HTTP status code associated with the success.
    message (str): A human-readable message describing the success.
    res_data (any, optional): Additional data associated with the \
        success response (default is None).

    Methods:
        get_json(): Returns a dictionary representing the success response in JSON format.

    Example:
        success_response = SuccessResponse(status_code=200,\
              message="Request successful", res_data={"key": "value"})
        success_data = success_response.get_json()
    """

    success = True

    def __init__(self, status_code, message, res_data=None):
        self.status_code = status_code
        self.message = message
        self.res_data = res_data

    def get_json(self):
        """
        Returns a dictionary representing the success response in JSON format.

        Returns:
            dict: A dictionary with keys 'success', 'status_code', 'message', and 'data'.
                  The 'data' key contains a dictionary with the optional response data.
        """
        return {
            "success": SuccessResponse.success,
            "status_code": self.status_code,
            "message": self.message,
            "data": {"json": [self.res_data]},
        }
