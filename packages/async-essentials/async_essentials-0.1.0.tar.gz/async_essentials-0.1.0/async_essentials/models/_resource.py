import typing

from pydantic import BaseModel

from .._request import EssentialsRequest


class Resource(BaseModel):
    """The basics of an API resource."""

    _request: typing.Optional[EssentialsRequest]

    class Config:
        arbitrary_types_allowed = True
        underscore_attrs_are_private = True

    @property
    def fetched(self) -> bool:
        """Flag to indicate that the resource has been fetched by the client endpoint/transport layer.
        This enables the model to have its own IO interactions."""
        return self._request is not None
