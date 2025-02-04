from http import HTTPStatus

def success_response(status_code: int = HTTPStatus.OK.value, details: str = "", data = None) -> dict :
    response = {
        "status_code": status_code,
        "details": details
    }
    if data is not None:
        response["data"] = data

    return response


class CustomException(Exception):
    def __init__(self, status_code: int, details: str):
        super().__init__(details)
        self.status_code = status_code
        self.details = details

    def __str__(self):
        return f"{self.status_code}: {self.details}"


def error_response(status_code, details):
    response = {
        "status_code": status_code,
        "details": details
    }
    return response
