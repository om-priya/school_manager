from flask import jsonify


class ErrorResponse:
    success = False

    def __init__(self, status_code, message):
        self.err_status_code = status_code
        self.err_message = message

    def get_json(self):
        return {
            "success": ErrorResponse.success,
            "err_status_code": self.err_status_code,
            "err_message": self.err_message,
        }


class SuccessResponse:
    success = True

    def __init__(self, status_code, message, res_data=None):
        self.status_code = status_code
        self.message = message
        self.res_data = res_data

    def get_json(self):
        return {
            "success": SuccessResponse.success,
            "status_code": self.status_code,
            "message": self.message,
            "data": {"json": self.res_data},
        }
