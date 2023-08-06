import logging

from ._auth import EssentialsAuth
from ._auth import EssentialsEnvAuth
from ._client import Essentials
from ._exceptions import AuthEnvironmentException
from ._exceptions import AuthUsernameNotEmailException
from ._exceptions import BadRequest400Exception
from ._exceptions import BadTimeoutException
from ._exceptions import Conflicted409Exception
from ._exceptions import EssentialsException
from ._exceptions import Forbidden403Exception
from ._exceptions import NotFound404Exception
from ._exceptions import ServerError500Exception
from ._exceptions import Unauthorized401Exception
from ._exceptions import UnknownResponseException
from ._exceptions import Unprocessable422Exception
from .models import ProductPurchaseInfoResponseResource
from .models import ProductResponseResource

# logging is an application-wide task; add a null handler and nothing else.
logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__ = (
    "Essentials",
    "EssentialsAuth",
    "ProductPurchaseInfoResponseResource",
    "Unauthorized401Exception",
    "ProductResponseResource",
    "Forbidden403Exception",
    "Conflicted409Exception",
    "EssentialsException",
    "AuthEnvironmentException",
    "NotFound404Exception",
    "ServerError500Exception",
    "BadRequest400Exception",
    "Unprocessable422Exception",
    "UnknownResponseException",
    "EssentialsEnvAuth",
    "AuthUsernameNotEmailException",
    "BadTimeoutException",
)
