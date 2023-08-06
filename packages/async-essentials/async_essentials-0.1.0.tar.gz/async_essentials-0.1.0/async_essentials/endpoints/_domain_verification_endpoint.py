from async_essentials._protocols import Transportable


class DomainVerificationEndpoint:
    """Entrypoint into the /api/v1/domains (verification) endpoint of the API."""

    def __init__(self, client: Transportable) -> None:
        self.client = client
