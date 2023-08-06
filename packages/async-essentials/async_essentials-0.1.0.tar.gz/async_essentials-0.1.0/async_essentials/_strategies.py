import typing

from ._exceptions import BadRequest400Exception
from ._exceptions import Conflicted409Exception
from ._exceptions import Forbidden403Exception
from ._exceptions import NotFound404Exception
from ._exceptions import ServerError500Exception
from ._exceptions import Unauthorized401Exception
from ._exceptions import UnknownResponseException
from ._exceptions import Unprocessable422Exception
from ._response import EssentialsResponse
from ._types import StrategyMapAlias


async def success_strategy(response: EssentialsResponse) -> EssentialsResponse:
    """A simple strategy for handling success, pass the response on to be wrapped."""
    return response


async def bad_request_strategy(response: EssentialsResponse) -> EssentialsResponse:
    """Handles 400 API responses by default."""
    raise BadRequest400Exception()


async def unauthorized_strategy(response: EssentialsResponse) -> typing.NoReturn:
    """Handles 401 API responses by default."""
    x_user_header = response.request.headers["X-USER"]  # type: ignore [index]
    raise Unauthorized401Exception(f"Incorrect password provided for {x_user_header} or they are not an admin")


async def forbidden_strategy(response: EssentialsResponse) -> typing.NoReturn:
    """Handles 403 API responses by default."""
    x_user_header = response.request.headers["X-USER"]  # type: ignore [index]
    raise Forbidden403Exception(f"User({x_user_header}) is forbidden for this request")


async def not_found_strategy(response: EssentialsResponse) -> typing.NoReturn:
    """Handles 404 API responses by default."""
    raise NotFound404Exception(f"{response.request.url} was not a valid path")


async def conflicted_strategy(response: EssentialsResponse) -> typing.NoReturn:
    """Handles 409 API responses by default."""
    raise Conflicted409Exception("Attempted to create an essentials resource that already existed")


async def unprocessable_strategy(response: EssentialsResponse) -> typing.NoReturn:
    """Handles 422 API responses by default."""
    raise Unprocessable422Exception()  # Todo: Error message/response content?


async def internal_error_strategy(response: EssentialsResponse) -> typing.NoReturn:
    """Handles 500 API responses by default."""
    raise ServerError500Exception("500 Internal Server Error")


async def unknown_response_strategy(response: EssentialsResponse) -> typing.NoReturn:
    """Handles everything not documented in the essentials API specification by default."""
    raise UnknownResponseException(f"Unknown response: {response.status_code}.")


STATUS_HANDLERS: StrategyMapAlias = {
    200: success_strategy,
    201: success_strategy,
    400: bad_request_strategy,
    401: unauthorized_strategy,
    403: forbidden_strategy,
    404: not_found_strategy,
    409: conflicted_strategy,
    422: unprocessable_strategy,
    500: internal_error_strategy,
}
