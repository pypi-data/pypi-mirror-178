from async_essentials._protocols import Transportable


class DomainsEndpoint:
    """Entrypoint into the /api/v1/domains endpoint of the API."""

    def __init__(self, client: Transportable) -> None:
        self.client = client
