from .._protocols import Transportable
from ..models import MeResource
from ._route import RouteTemplate


class MeEndpoint:
    """Entrypoint into the /api/v1/me endpoint of the API."""

    FetchRoute = RouteTemplate("/me")

    def __init__(self, client: Transportable) -> None:
        self.client = client

    async def get(self) -> MeResource:
        """Retrieve metadata about the logged in user."""
        response = await self.client.get(url=self.FetchRoute())
        return response.deserialize(MeResource)
