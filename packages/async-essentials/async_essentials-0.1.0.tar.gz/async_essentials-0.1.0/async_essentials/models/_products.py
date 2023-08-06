import typing

from ._resource import Resource


class ProductVariantResponseResource(Resource):
    """Definition of an Essentials Product Variant."""

    name: str
    ref: str
    order_index: int
    description: str
    is_purchasable: bool


class ProductPurchaseInfoResponseResource(Resource):
    """Purchase details related to this Product, may be null if not purchased."""

    when_added: str
    variant: str
    when_renewal: str
    when_status_updated: str
    auto_renew: bool
    trial_variant: str
    is_trial: bool
    trial_end_date: str


class ProductResponseResource(Resource):
    """Definition of an Essentials Product, including purchase info if applicable."""

    status: str
    label: str
    name: str
    description: str
    billing_method: str
    min_term: int
    is_renewable: bool
    min_licenses: int
    help_url: str
    variants: typing.List[ProductVariantResponseResource]
    purchase_info: typing.Optional[ProductPurchaseInfoResponseResource]


class ProductResource(Resource):
    """Encapsulation of a `Product` resource."""

    label: str
    variant: str
    auto_renew: bool
    is_trial: bool
