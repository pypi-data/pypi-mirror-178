from async_essentials._protocols import Transportable


class PackageEndpoint:
    """Entrypoint into the /api/v1/package endpoint of the API."""

    def __init__(self, client: Transportable) -> None:
        self.client = client
