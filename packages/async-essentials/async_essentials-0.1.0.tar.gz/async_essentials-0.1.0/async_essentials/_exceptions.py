import typing


class EssentialsException(Exception):
    """The base async essentials exception."""


class BadRequest400Exception(EssentialsException):
    """Indicate that the request was malformed.  Likely a bug in the wrapper itself."""


class Unauthorized401Exception(EssentialsException):
    """Indicate that essentials did not accept the EssentialsAuth credentials provided."""


class Forbidden403Exception(EssentialsException):
    """Indicate the authenticated user is performing actions that they are not permitted for."""


class NotFound404Exception(EssentialsException):
    """Indicate that the essentials path did not exist."""


class Conflicted409Exception(EssentialsException):
    """Indicate the user is trying to create a resource that already exists."""


class Unprocessable422Exception(EssentialsException):  # noqa (keep IDE happy with spelling).
    """Indicate that essentials refused the resource update/create due to invalid data."""


class ServerError500Exception(EssentialsException):
    """A 500 response code was returned by essentials."""


class AuthUsernameNotEmailException(EssentialsException):
    """Raised when the X-USER header does not (softly) conform to a simple email check."""


class AuthEnvironmentException(EssentialsException):
    """Using EssentialsEnvironAuth without the keys to lookup being available in the environment."""


class UnknownResponseException(EssentialsException):
    """Raised when the response code is not one publically advertised by essentials API specification."""


class BadTimeoutException(EssentialsException):
    """Raised when values passed for read, write or connect timeouts are not sufficient."""

    def __init__(self, timeout: typing.Any) -> None:
        super().__init__(f"{timeout!r} must be a float or integer that is greater than 0.")
