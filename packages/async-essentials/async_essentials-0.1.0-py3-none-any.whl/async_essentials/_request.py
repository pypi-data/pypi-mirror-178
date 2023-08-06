import httpx

from ._mixins import DelegateMixin


class EssentialsRequest(DelegateMixin):
    """A request instance that is replayable.  It keeps track of the transport layer that
    initially was used for dispatching it and can replay itself."""

    def __init__(self, request: httpx.Request) -> None:
        self.delegate = request

    @property
    def request(self) -> httpx.Request:
        return self.delegate
