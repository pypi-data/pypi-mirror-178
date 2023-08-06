import logging
import typing

import httpx

from ._mixins import DelegateMixin
from ._request import EssentialsRequest
from .models import Resource

logger = logging.getLogger(__name__)


T = typing.TypeVar("T", bound=Resource)


class EssentialsResponse(DelegateMixin):
    """A Custom wrapped response.  This is used heavily for auto deserialization of responses
    into pydantic model classes."""

    def __init__(self, delegate: httpx.Response, model: typing.Optional[typing.Type[Resource]] = None) -> None:
        self._delegate = delegate
        self._created_by = EssentialsRequest(self._delegate.request)
        self._model = model
        logger.debug(f"Response received: {self._delegate.status_code=}, {self._delegate.request.url}")

    @property
    def status_code(self) -> int:
        """Retrieve the response status code."""
        return self._delegate.status_code

    @property
    def reason_phrase(self) -> str:
        return self._delegate.reason_phrase

    @property
    def http_version(self) -> str:
        return self._delegate.http_version

    @property
    def url(self) -> str:
        return str(self._delegate.url)

    @property
    def request(self) -> EssentialsRequest:
        return self._created_by

    def json(self, **kwargs: typing.Any) -> typing.Any:
        return self._delegate.json(**kwargs)

    def deserialize(self, clazz: typing.Type[T], **kwargs) -> T:
        """Load the response into a corresponding resource.  When deserializing to any model, the model
        instance will be passed the request instance that was used to retrieve it initially.  This allows
        us to get somewhat replay-ability for things which need to refetch themselves on the model directly.

        :param clazz: The Resource (class not instance) to instantiate with the response payload."""
        response_payload = self._delegate.json(**kwargs)
        logger.debug(f"Attempting to shovel: {response_payload=} into {clazz.__name__}")
        model_instance = clazz(_request=self._created_by, **response_payload)
        return model_instance
