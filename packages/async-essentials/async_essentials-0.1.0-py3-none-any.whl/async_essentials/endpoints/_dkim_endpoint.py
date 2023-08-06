from async_essentials._protocols import Transportable


class DkimEndpoint:
    """Entrypoint into the /api/v1/dkim endpoint of the API."""

    def __init__(self, client: Transportable) -> None:
        self.client = client
