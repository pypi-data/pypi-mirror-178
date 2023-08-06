import typing

from ._resource import Resource


class FeaturesResource(Resource):
    """Encapsulation of a `Features` resource."""

    attachment_defense: typing.Optional[bool]
    dlp: typing.Optional[bool]
    email_encryption: typing.Optional[bool]
    social_media_account_protection: typing.Optional[bool]
    outbound_relaying: typing.Optional[bool]
    instant_replay: typing.Optional[int]
    email_archive: typing.Optional[bool]
    url_defense: typing.Optional[bool]
    disclaimers: typing.Optional[bool]
    smtp_discovery: typing.Optional[bool]
