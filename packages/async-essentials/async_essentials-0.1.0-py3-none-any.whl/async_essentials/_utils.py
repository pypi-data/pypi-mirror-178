import re
import typing

from ._exceptions import BadTimeoutException


def copy_map_without_keys(mapping, omit: typing.Tuple[str, ...] = ()) -> typing.Dict[typing.Any, typing.Any]:
    """Creates a copy of the mapping removing keys that match those in omit.

    :param mapping: A mapping to copy from.
    :param omit: A tuple of keys to exclude from the returned mapping.
    """
    return {k: v for k, v in mapping.items() if k not in omit}


# https://stackoverflow.com/questions/8022530/how-to-check-for-valid-email-address
SIMPLE_MAIL_PATTERN = re.compile(r"[^@]+@[^@]+\.[^@]+")


def is_email(email: str) -> bool:
    """Utility method for checking if a string conforms to an email address.  This is a light approximation
    and is sufficient for the library as determining this in a guaranteed way is a lot harder than it seems.

    :param email: The email addr to validate.
    """
    return bool(SIMPLE_MAIL_PATTERN.fullmatch(email))


def validate_timeout(timeout: typing.Union[int, float]) -> typing.Union[int, float]:
    """Validate that the number provided is either an int or float and is greater than 0.

    :param timeout: The number to check."""
    if not isinstance(timeout, (int, float)) or not timeout > 0:
        raise BadTimeoutException(timeout)
    return timeout
