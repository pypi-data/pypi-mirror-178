from dataclasses import dataclass


@dataclass(frozen=True)
class UserType:
    """Representation of all supported user types."""

    oem_partner_admin = "oem_partner_admin"
    strategic_partner_admin = "strategic_partner_admin"
    channel_admin = "channel_admin"
    organization_admin = "organization_admin"
    end_user = "end_user"
    silent_user = "silent_user"
    functional_account = "functional_account"


@dataclass(frozen=True)
class EntityType:
    """Representation of all supported entity types."""

    oem_partner = "oem_partner"
    strategic_partner = "strategic_partner"
    channel = "channel"
    organization = "organization"


@dataclass(frozen=True)
class ProductLabel:
    """Representation of all support product label types."""

    available = "available"
    provisioning = "provisioning"
    requires_user_action = "requires_user_action"
    error = "error"
    confirmed = "confirmed"
    cancelled = "cancelled"
    deleting = "deleting"
