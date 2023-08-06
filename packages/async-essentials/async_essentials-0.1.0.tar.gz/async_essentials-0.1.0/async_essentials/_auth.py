from __future__ import annotations

import os
import typing

from httpx import Auth
from httpx import Request

from async_essentials._exceptions import AuthEnvironmentException
from async_essentials._exceptions import AuthUsernameNotEmailException

from ._utils import is_email


class EssentialsAuth(Auth):
    def __init__(self, *, username: str, password: str) -> None:
        """
        A simple essentials based authentication mechanism for appending appropriate HTTP headers.
        This auth mechanism is entirely synchronous.

        :param username: The X-USER header value
        :param password: The X-PASSWORD header value
        """
        self.username = username
        if not is_email(self.username):
            raise AuthUsernameNotEmailException(f"{self.username} is not a valid email addr for X-USER.")
        self.password = password

    def auth_flow(self, request: Request) -> typing.Generator[None, Request, None]:
        """
        Handles X-USER and X-PASSWORD headers for authenticating with the essentials
        API.
        :param request: The httpx Request object.
        """
        request.headers["X-USER"] = self.username
        request.headers["X-PASSWORD"] = self.password
        yield request

    @classmethod
    def from_sequence(cls, sequence: typing.Sequence[str]) -> EssentialsAuth:
        """Alternative constructor from a length 2 sequence"""
        if len(sequence) != 2:
            raise ValueError(f"{sequence} did not contain both a username and password in that order.")
        username, password = sequence
        params = {"username": username, "password": password}
        return cls(**params)


class EssentialsEnvAuth(Auth):
    def __init__(self, *, user_lookup: str, password_lookup: str) -> None:
        """A simple auth mechanism that lookups' user provided keys from the
        environment for both the username and password, this allows flexibility
        without enforcing a strict key ourselves.

        :param user_lookup: The name of the env variable housing the X-USER value
        :param password_lookup: The name of the env variable housing the X-PASSWORD value"""
        self.user_lookup = user_lookup
        self.password_lookup = password_lookup

    def auth_flow(self, request: Request) -> typing.Generator[Request, Request, None]:
        request.headers["X-USER"] = self._lookup(self.user_lookup)
        request.headers["X-PASSWORD"] = self._lookup(self.password_lookup)
        yield request

    @staticmethod
    def _lookup(key: str) -> str:
        if key not in os.environ:
            raise AuthEnvironmentException(f"{key=} is not available in the environment.")
        return os.environ[key]
