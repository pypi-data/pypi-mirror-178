from async_essentials._protocols import Transportable


class LicensingEndpoint:
    """Entrypoint into the /api/v1/licensing endpoint of the API."""

    def __init__(self, client: Transportable) -> None:
        self.client = client
