import typing

import httpx

from ._response import EssentialsResponse
from ._strategies import STATUS_HANDLERS
from ._strategies import unknown_response_strategy
from ._types import StrategyMapAlias


class ResponseEnforcer:
    """Default response handler, makes sensible decisions about various essentials responses.

    :param overrides: user defined overrides to replace for various status codes.  Format should be
    a mapping where the key is the status code you wish to register a handler for (or replace an existing)
    handler for.  The value should be a coroutine to be awaited internally and passed the httpx.Response
    object.
    """

    def __init__(self, *, overrides: typing.Optional[StrategyMapAlias] = None) -> None:
        if overrides is None:
            overrides = {}
        self.factory = {**STATUS_HANDLERS, **overrides}  # type: ignore [arg-type]

    async def handle_response(self, response: EssentialsResponse) -> EssentialsResponse:
        """Handle responses from the essentials' server."""
        status_code = response.status_code
        handler = self.factory.get(status_code, unknown_response_strategy)
        _ = self._parse_response_content(response)  # noqa (unused for now)
        return await handler(response)

    @staticmethod
    def _parse_response_content(response: httpx.Response) -> typing.Dict[typing.Any, typing.Any]:
        """Attempt to parse the json response to shovel the essentials errors through to
        the custom wrapper exceptions."""
        try:
            return response.json()  # Todo: Error handling ofc.
        except Exception:
            return {}
