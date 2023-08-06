from async_essentials._protocols import Transportable

from .._response import EssentialsResponse
from ..models import ProductResource
from ..models import ProductResponseResource
from ._route import RouteTemplate


class ProductsEndpoint:
    """Entrypoint into the /api/v1/products endpoint of the API."""

    FetchAllProducts = RouteTemplate("/orgs/$domain/products")
    CreateProduct = FetchAllProducts
    FetchSingleProduct = RouteTemplate("/orgs/$domain/products/$label")
    DeleteProduct = FetchSingleProduct
    PatchProduct = FetchSingleProduct

    def __init__(self, client: Transportable) -> None:
        self.client = client

    async def get(self, domain: str, label: str) -> ProductResponseResource:
        """Fetch a single product.

        :param domain: The domain of the entity.
        :param label: The product label to filter on.
        """
        response = await self.client.get(url=self.FetchSingleProduct(domain=domain, label=label))
        return response.deserialize(clazz=ProductResponseResource)

    async def get_all(self, domain: str) -> EssentialsResponse:
        """Retrieve all products

        :param domain: The domain name for the entity.
        """
        return await self.client.get(self.FetchAllProducts(domain=domain))

    async def create(self, domain: str, product: ProductResource) -> EssentialsResponse:
        """Create a new product resource.

        :param domain: The domain name for the entity.
        :param product: A :class:`ProductResource` instance to serialise and send."""
        return await self.client.post(url=self.CreateProduct(domain=domain), json=product.json())

    async def delete(self, domain: str, label: str) -> EssentialsResponse:
        """Delete a product resource.

        :param domain: The domain name for the entity.
        :param label: The product label (type) to delete."""
        return await self.client.delete(self.DeleteProduct(domain=domain, label=label))

    async def patch(self, domain: str, label: str) -> EssentialsResponse:
        """Patch a product resource."""
        return await self.client.patch(self.PatchProduct(domain=domain, label=label))
