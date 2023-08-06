from async_essentials._protocols import Transportable


class SenderListsEndpoint:
    """Entrypoint into the /api/v1/sender-lists endpoint of the API."""

    def __init__(self, client: Transportable) -> None:
        self.client = client
