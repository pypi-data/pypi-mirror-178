from async_essentials._protocols import Transportable

from ..models import FeaturesResource


class FeaturesEndpoint:
    """Entrypoint into the /api/v1/features endpoint of the API."""

    def __init__(self, client: Transportable) -> None:
        self.client = client

    async def get(self, domain: str) -> FeaturesResource:  # type: ignore
        """Fetch Features for the domain."""
        pass
