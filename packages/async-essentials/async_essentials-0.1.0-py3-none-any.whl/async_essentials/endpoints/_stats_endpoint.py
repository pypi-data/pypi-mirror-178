from async_essentials._protocols import Transportable


class StatsEndpoint:
    """Entrypoint into the /api/v1/stats endpoint of the API."""

    def __init__(self, client: Transportable) -> None:
        self.client = client
