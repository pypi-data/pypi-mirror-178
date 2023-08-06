from async_essentials._protocols import Transportable


class SettingsEndpoint:
    """Entrypoint into the /api/v1/settings endpoint of the API."""

    def __init__(self, client: Transportable) -> None:
        self.client = client
