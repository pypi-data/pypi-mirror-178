from async_essentials._protocols import Transportable


class EmailTaggingEndpoint:
    """Entrypoint into the /api/v1/email-tagging endpoint of the API."""

    def __init__(self, client: Transportable) -> None:
        self.client = client
