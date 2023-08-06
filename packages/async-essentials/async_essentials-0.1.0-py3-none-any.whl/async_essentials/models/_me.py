import typing

from pydantic import Field

from .._mixins import FetchableMixin
from ._products import Resource


class MeResource(Resource, FetchableMixin):
    """Encapsulation of a `Me` resource."""

    user_id: typing.Optional[int]
    firstname: str
    surname: str
    primary_email: str
    user_type: str = Field(alias="type")
    is_admin: bool
    is_partner_admin: bool
    entity_id: int
    entity_primary_domain: str
    entity_type: str
    read_only_user: bool
