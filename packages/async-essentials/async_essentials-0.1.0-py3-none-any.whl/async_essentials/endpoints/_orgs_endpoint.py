from async_essentials._protocols import Transportable


class OrgsEndpoint:
    """Entrypoint into the /api/v1/orgs endpoint of the API."""

    def __init__(self, client: Transportable) -> None:
        self.client = client
