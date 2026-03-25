from fastapi import HTTPException, status


class CustomException(HTTPException):
    """Base HTTP exception used for application-level API errors."""

    def __init__(self, status_code: int, detail: str) -> None:
        super().__init__(status_code=status_code, detail=detail)


class BadRequestException(CustomException):
    def __init__(self, detail: str = "Bad request.") -> None:
        super().__init__(status.HTTP_400_BAD_REQUEST, detail)


class UnauthorizedException(CustomException):
    def __init__(self, detail: str = "Unauthorized.") -> None:
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail)


class ForbiddenException(CustomException):
    def __init__(self, detail: str = "Forbidden.") -> None:
        super().__init__(status.HTTP_403_FORBIDDEN, detail)


class NotFoundException(CustomException):
    def __init__(self, detail: str = "Not found.") -> None:
        super().__init__(status.HTTP_404_NOT_FOUND, detail)


class UnprocessableEntityException(CustomException):
    def __init__(self, detail: str = "Unprocessable entity.") -> None:
        super().__init__(status.HTTP_422_UNPROCESSABLE_ENTITY, detail)


class DuplicateValueException(CustomException):
    def __init__(self, detail: str = "Duplicate value.") -> None:
        super().__init__(status.HTTP_409_CONFLICT, detail)


class RateLimitException(CustomException):
    def __init__(self, detail: str = "Rate limit exceeded.") -> None:
        super().__init__(status.HTTP_429_TOO_MANY_REQUESTS, detail)
