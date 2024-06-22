from fastapi.exceptions import HTTPException
from starlette import status


class NotFoundException(HTTPException):
    def __init__(
        self,
        detail: any = None,
    ):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = detail


class TimeoutException(HTTPException):
    def __init__(
        self,
        detail: any = None,
    ):
        self.status_code = status.HTTP_408_REQUEST_TIMEOUT
        self.detail = detail


class UnprocessableEntityException(HTTPException):
    def __init__(
        self,
        detail: any = None,
    ):
        self.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        self.detail = detail


class BadRequestException(HTTPException):
    def __init__(
        self,
        detail: any = None,
    ):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = detail
