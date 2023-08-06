from async_essentials._protocols import Transportable


class TokenEndpoint:
    """Entrypoint into the /api/v1/token endpoint of the API."""

    def __init__(self, client: Transportable) -> None:
        self.client = client
