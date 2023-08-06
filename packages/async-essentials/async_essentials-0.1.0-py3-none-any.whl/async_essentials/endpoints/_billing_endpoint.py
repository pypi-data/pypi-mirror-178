from async_essentials._protocols import Transportable


class BillingEndpoint:
    """Entrypoint into the /api/v1/billing endpoint of the API."""

    def __init__(self, client: Transportable) -> None:
        self.transport = client
