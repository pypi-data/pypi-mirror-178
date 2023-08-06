from async_essentials._protocols import Transportable


class EndpointsEndpoint:
    """Entrypoint into the /api/v1/endpoints endpoint of the API."""

    def __init__(self, client: Transportable) -> None:
        self.client = client
