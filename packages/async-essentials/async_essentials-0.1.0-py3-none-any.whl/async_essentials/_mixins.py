import typing

T = typing.TypeVar("T")


class HasTransport(typing.Protocol):
    @property
    def _transport(self):
        ...


class FetchableMixin:
    """A Mixin class that allows an API model to refresh itself.  Subclasses of `Resource` can benefit
    from all API mixin classes."""

    async def refresh(self):
        ...


class DelegateMixin:
    """Bolts on automatic delegation to any classes that are wrapping a `delegate` instance attribute."""

    def __getattr__(self, name: str) -> typing.Union[typing.Any, typing.Callable[[typing.Any], typing.Any]]:
        attr = getattr(self.delegate, name)
        if not callable(attr):
            return attr

        def wrapper(*args, **kwargs):
            return attr(*args, **kwargs)

        return wrapper
