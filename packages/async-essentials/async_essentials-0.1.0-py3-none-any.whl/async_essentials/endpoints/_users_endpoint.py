from async_essentials._protocols import Transportable


class UsersEndpoint:
    """Entrypoint into the /api/v1/users endpoint of the API."""

    def __init__(self, client: Transportable) -> None:
        self.client = client
