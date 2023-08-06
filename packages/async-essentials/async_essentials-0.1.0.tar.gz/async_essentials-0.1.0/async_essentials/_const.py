from dataclasses import dataclass


@dataclass(frozen=True)
class Environment:
    US1 = "us1"
    US2 = "us2"
    US3 = "us3"
    US4 = "us4"
    US5 = "us5"
    EU1 = "eu1"


@dataclass(frozen=True)
class HttpVerb:
    GET: str = "get"
    POST: str = "post"
    PUT: str = "put"
    DELETE: str = "delete"
    PATCH: str = "patch"
