from async_essentials._protocols import Transportable


class ReportingEndpoint:
    """Entrypoint into the /api/v1/reporting endpoint of the API."""

    def __init__(self, client: Transportable) -> None:
        self.client = client
