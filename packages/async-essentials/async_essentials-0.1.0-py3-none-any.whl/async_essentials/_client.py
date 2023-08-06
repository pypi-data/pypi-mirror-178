from __future__ import annotations

import logging
import types
import typing

import httpx

from ._auth import EssentialsAuth
from ._const import HttpVerb
from ._enforcer import ResponseEnforcer
from ._response import EssentialsResponse
from ._types import CookieTypes
from ._types import HeaderTypes
from ._types import JsonType
from ._types import ProxyTypes
from ._types import QueryParamTypes
from ._types import RequestContent
from ._types import RequestData
from ._types import RequestFiles
from ._types import StrategyMapAlias
from ._utils import validate_timeout
from .endpoints import AuthenticationEndpoint
from .endpoints import BillingEndpoint
from .endpoints import DkimEndpoint
from .endpoints import DomainsEndpoint
from .endpoints import DomainVerificationEndpoint
from .endpoints import EmailTaggingEndpoint
from .endpoints import EndpointsEndpoint
from .endpoints import FeaturesEndpoint
from .endpoints import LicensingEndpoint
from .endpoints import MeEndpoint
from .endpoints import OrgsEndpoint
from .endpoints import PackageEndpoint
from .endpoints import ProductsEndpoint
from .endpoints import ReportingEndpoint
from .endpoints import SenderListsEndpoint
from .endpoints import SettingsEndpoint
from .endpoints import StatsEndpoint
from .endpoints import TokenEndpoint
from .endpoints import UsersEndpoint

logger = logging.getLogger(__name__)


# Todo: Wrapping the context manager (AsyncClient) doesn't seem 100%.


class Essentials:
    """
    An asynchronous API client for the proof point essentials V1 API.  This encapsulates all available
    endpoints as part of its facade.

    :param subdomain: The subdomain for the API (subdomains are incremental region numbers, e.g: us1, eu1, us3)
    :param auth: An instance of `EssentialsAuth` or a tuple of two strings used to decipher the X- headers.
    :param connect_timeout: Number of seconds to wait for the socket connection to be established before raising.
    :param read_timeout: Number of seconds to wait for a chunk of the response to be received before raising.
    :param write_timeout: Number of seconds to wait for a chunk of data to be sent before raising.
    :param proxies: (Optional) str or mapping of strings to route traffic through.
    :param response_enforcer: Callable for handling the API responses, defaults to the builtin ResponseEnforcer.
    :param response_handlers: Callables that adhere to a strategy for individual response codes.  The key should
    be an integer for a response code and the value should be an awaitable function that accepts an EssentialsResponse
    as a single argument and returns an EssentialsResponse.  This allows user defined code to customise the behaviour
    (often in the error/raising) cases and interject their own code.

    In the context of this class, a `session` is a httpx asynchronous client (not to be confused with a requests'
    session).  The essentials API at present does not support HTTP/2 communication, if that changes in future
    passing http2=True to the session will automatically enable all the benefits of that.

    Default utf-8 encoding is also assumed by the client here.

    For providing a robust API, The essentials client enforces a strict keyword only policy across its interface.
    This makes for easier refactoring in future at the (miniscule) cost of extra work on the client side.
    """

    def __init__(
        self,
        *,
        subdomain: str,
        auth: typing.Union[EssentialsAuth, typing.Tuple[str, str]],
        connect_timeout: float = 10.00,
        read_timeout: float = 10.00,
        write_timeout: float = 10.00,
        proxies: typing.Optional[ProxyTypes] = None,
        response_enforcer: typing.Type[ResponseEnforcer] = ResponseEnforcer,
        response_handlers: typing.Optional[StrategyMapAlias] = None,
    ) -> None:
        self.auth = auth if isinstance(auth, EssentialsAuth) else EssentialsAuth.from_sequence(auth)
        self.subdomain = subdomain
        self.connect_timeout = validate_timeout(connect_timeout)
        self.read_timeout = validate_timeout(read_timeout)
        self.write_timeout = validate_timeout(write_timeout)
        self.proxies = proxies
        self.response_enforcer = response_enforcer(overrides=response_handlers)
        self.session: httpx.AsyncClient = httpx.AsyncClient(
            auth=self.auth,
            base_url=f"http://{self.subdomain}/api/v1",  # Todo: Make this usable in reality AND in testing.
            timeout=httpx.Timeout(
                connect=self.connect_timeout, read=self.read_timeout, write=self.write_timeout, pool=None
            ),
            proxies=self.proxies,
        )

        # Api Routes
        self.authentication = AuthenticationEndpoint(self)
        self.settings = SettingsEndpoint(self)
        self.billing = BillingEndpoint(self)
        self.dkim = DkimEndpoint(self)
        self.domain_verification = DomainVerificationEndpoint(self)
        self.domains = DomainsEndpoint(self)
        self.email_tagging = EmailTaggingEndpoint(self)
        self.endpoints = EndpointsEndpoint(self)
        self.features = FeaturesEndpoint(self)
        self.licensing = LicensingEndpoint(self)
        self.me = MeEndpoint(self)
        self.orgs = OrgsEndpoint(self)
        self.package = PackageEndpoint(self)
        self.products = ProductsEndpoint(self)
        self.reporting = ReportingEndpoint(self)
        self.sender_lists = SenderListsEndpoint(self)
        self.stats = StatsEndpoint(self)
        self.token = TokenEndpoint(self)
        self.users = UsersEndpoint(self)

    async def _request(
        self,
        *,
        method: str,
        url: str,
        content: typing.Optional[RequestContent] = None,
        data: typing.Optional[RequestData] = None,
        files: typing.Optional[RequestFiles] = None,
        json: typing.Optional[JsonType] = None,
        params: typing.Optional[QueryParamTypes] = None,
        headers: typing.Optional[HeaderTypes] = None,
        cookies: typing.Optional[CookieTypes] = None,
    ) -> EssentialsResponse:
        """Build and send an HTTP request."""
        return await self._enforce_response(
            EssentialsResponse(
                await self.session.request(
                    method=method,
                    url=url,
                    content=content,
                    data=data,
                    files=files,
                    json=json,
                    params=params,
                    headers=headers,
                    cookies=cookies,
                )
            )
        )

    async def _send(self, request: httpx.Request) -> EssentialsResponse:
        """
        Send an unmodified request.
        """
        return EssentialsResponse(await self.session.send(request))

    async def _enforce_response(self, response: EssentialsResponse) -> EssentialsResponse:
        """Wrapper function to enforce and return the response instance.

        :param response: The already wrapped response object."""
        return await self.response_enforcer.handle_response(response)

    async def get(
        self,
        *,
        url: str,
        params: typing.Optional[QueryParamTypes] = None,
        headers: typing.Optional[HeaderTypes] = None,
        cookies: typing.Optional[CookieTypes] = None,
    ):
        """Dispatches an HTTP GET request.

        :param url:     The api routing suffix (after /api/v1/).
        :param params:  (Optional) Query string parameters to resolve into the url.
        :param headers: (Optional) headers to add to the request.
        :param cookies: (Optional) cookies to include with the request."""
        return await self._request(method=HttpVerb.GET, url=url, params=params, headers=headers, cookies=cookies)

    async def delete(
        self,
        *,
        url: str,
        params: typing.Optional[QueryParamTypes] = None,
        headers: typing.Optional[HeaderTypes] = None,
        cookies: typing.Optional[CookieTypes] = None,
    ) -> EssentialsResponse:
        """Dispatches an HTTP DELETE request.

        :param url:     The api routing suffix (after /api/v1/).
        :param params:  (Optional) Query string parameters to resolve into the url.
        :param headers: (Optional) headers to add to the request.
        :param cookies: (Optional) cookies to include with the request."""
        return await self._request(method=HttpVerb.DELETE, url=url, params=params, headers=headers, cookies=cookies)

    async def post(
        self,
        *,
        url: str,
        content: typing.Optional[RequestContent] = None,
        data: typing.Optional[RequestData] = None,
        files: typing.Optional[RequestFiles] = None,
        json: typing.Optional[JsonType] = None,
        params: typing.Optional[QueryParamTypes] = None,
        headers: typing.Optional[HeaderTypes] = None,
        cookies: typing.Optional[CookieTypes] = None,
    ) -> EssentialsResponse:
        """Dispatches an HTTP POST request.

        :param url:         The api routing suffix (after /api/v1/).
        :param content:     (Optional) Binary content to include in the request body (as bytes).
        :param data:        (Optional) Form data to include in the body of the request (as dictionary).
        :param files:       (Optional) A mapping of upload files to include in the request body.
        :param json:        (Optional) A JSON serializable object to include in the body of the request.
        :param params:      (Optional) Query string parameters to resolve into the url.
        :param headers:     (Optional) headers to add to the request.
        :param cookies:     (Optional) cookies to include with the request."""

        return await self._request(
            method=HttpVerb.POST,
            url=url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
        )

    async def put(
        self,
        *,
        url: str,
        content: typing.Optional[RequestContent] = None,
        data: typing.Optional[RequestData] = None,
        files: typing.Optional[RequestFiles] = None,
        json: typing.Optional[JsonType] = None,
        params: typing.Optional[QueryParamTypes] = None,
        headers: typing.Optional[HeaderTypes] = None,
        cookies: typing.Optional[CookieTypes] = None,
    ) -> EssentialsResponse:
        """Dispatches an HTTP PUT request.

        :param url:         The api routing suffix (after /api/v1/).
        :param content:     (Optional) Binary content to include in the request body (as bytes).
        :param data:        (Optional) Form data to include in the body of the request (as dictionary).
        :param files:       (Optional) A mapping of upload files to include in the request body.
        :param json:        (Optional) A JSON serializable object to include in the body of the request.
        :param params:      (Optional) Query string parameters to resolve into the url.
        :param headers:     (Optional) headers to add to the request.
        :param cookies:     (Optional) cookies to include with the request."""
        return await self._request(
            method=HttpVerb.PUT,
            url=url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
        )

    async def patch(
        self,
        *,
        url: str,
        content: typing.Optional[RequestContent] = None,
        data: typing.Optional[RequestData] = None,
        files: typing.Optional[RequestFiles] = None,
        json: typing.Optional[JsonType] = None,
        params: typing.Optional[QueryParamTypes] = None,
        headers: typing.Optional[HeaderTypes] = None,
        cookies: typing.Optional[CookieTypes] = None,
    ) -> EssentialsResponse:
        """Dispatches an HTTP PATCH request.

        :param url:         The api routing suffix (after /api/v1/).
        :param content:     (Optional) Binary content to include in the request body (as bytes).
        :param data:        (Optional) Form data to include in the body of the request (as dictionary).
        :param files:       (Optional) A mapping of upload files to include in the request body.
        :param json:        (Optional) A JSON serializable object to include in the body of the request.
        :param params:      (Optional) Query string parameters to resolve into the url.
        :param headers:     (Optional) headers to add to the request.
        :param cookies:     (Optional) cookies to include with the request."""
        return await self._request(
            method=HttpVerb.PATCH,
            url=url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
        )

    async def __aenter__(self) -> Essentials:
        """Enter the async client context."""
        return self

    async def __aexit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]] = None,
        exc_val: typing.Optional[BaseException] = None,
        exc_tb: typing.Optional[types.TracebackType] = None,
    ) -> None:
        """Try and close the underlying httpx session."""
        await self.session.__aexit__(exc_type, exc_val, exc_tb)
