import typing

from async_essentials._response import EssentialsResponse

UrlTypes: str
QueryParamTypes = typing.Mapping[str, typing.Any]
RequestContent = typing.Mapping[str, typing.Any]
RequestData = typing.Mapping[str, typing.Any]
RequestFiles = typing.Any
JsonType = typing.Any
HeaderTypes = typing.Union[typing.Mapping[str, str], typing.Mapping[bytes, bytes]]
CookieTypes = typing.Mapping[str, str]
ProxyTypes = typing.Union[str, typing.Mapping[str, str]]


RoutesMappingType = typing.Dict[str, str]


ModelPayloadType = typing.Dict[str, typing.Any]
StrategyAlias = typing.Callable[[EssentialsResponse], typing.Awaitable[typing.Any]]
StrategyMapAlias = typing.Dict[int, StrategyAlias]
