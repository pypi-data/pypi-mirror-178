import abc
from typing import Protocol
from typing import runtime_checkable

from async_essentials._response import EssentialsResponse


class Deserializable(Protocol):
    """Interface for something which can be deserialised to a model."""

    @abc.abstractmethod
    async def deserialize(self):
        raise NotImplementedError


class HandlesResponse(Protocol):
    """Interface for handling HTTP Responses."""

    @abc.abstractmethod
    async def handle_response(self, response: EssentialsResponse):
        raise NotImplementedError


@runtime_checkable
class Transportable(Protocol):
    """Interface for dispatching HTTP requests."""

    @abc.abstractmethod
    async def get(self, *args, **kwargs) -> EssentialsResponse:
        raise NotImplementedError

    @abc.abstractmethod
    async def post(self, *args, **kwargs) -> EssentialsResponse:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, *args, **kwargs) -> EssentialsResponse:
        raise NotImplementedError

    @abc.abstractmethod
    async def patch(self, *args, **kwargs) -> EssentialsResponse:
        raise NotImplementedError

    @abc.abstractmethod
    async def put(self, *args, **kwargs) -> EssentialsResponse:
        raise NotImplementedError


#    @abc.abstractmethod
#   async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
#        raise NotImplementedError
