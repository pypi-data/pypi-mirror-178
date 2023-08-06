from async_essentials._protocols import Transportable


class AuthenticationEndpoint:
    """Entrypoint into the /api/v1/authentication endpoint of the API."""

    def __init__(self, client: Transportable) -> None:
        self.client = client
