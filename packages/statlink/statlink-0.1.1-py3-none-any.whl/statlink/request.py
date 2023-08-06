from __future__ import annotations
import typing
import asyncio
from enum import Enum

from .response import Response

if typing.TYPE_CHECKING:
    from .engine import Engine


class RequestState(Enum):
    NOT_STARTED = 0
    IN_PROGRESS = 1
    SUCCESS = 2
    ERROR = 3

    def __lt__(self, other: "RequestState"):
        return self.value < other.value


class RequestError(Exception):
    pass


class RequestTimeoutError(RequestError):

    def __str__(self) -> str:
        return "Request timeout"


class RequestConnectionError(RequestError):

    def __str__(self) -> str:
        return "Connection error"


class Request:
    def __init__(
        self,
        url: str,
        max_retry: int = 1,
        timeout: int = 20,
        depth: int = 0
    ):
        self.url = url
        self.max_retry = max_retry
        self.timeout = timeout
        self.state = RequestState.NOT_STARTED
        self.depth = depth
        self.response = None
        self.error = None
        self.duration = None
        self.retry_count = -1

    async def fetch(self, engine: "Engine") -> Response:
        loop = asyncio.get_running_loop()
        self.state = RequestState.IN_PROGRESS
        while self.retry_count < self.max_retry:
            self.retry_count += 1
            start_time = loop.time()
            try:
                self.response = await engine.fetch(request=self)
                self.error = None
            except RequestError as request_error:
                self.error = request_error
            self.duration = loop.time() - start_time
            if self.response:
                self.state = RequestState.SUCCESS
                return self.response
        self.state = RequestState.ERROR

    @property
    def ok(self) -> bool:
        return self.response is not None and self.response.ok

    @property
    def completed(self) -> bool:
        return self.state in [RequestState.SUCCESS, RequestState.ERROR]

    def result(self) -> str:
        content = self.response and self.response.status or self.error
        if self.completed:
            return f"{self.url} {content} {self.duration}"
        elif self.state is RequestState.IN_PROGRESS:
            retry = (
                f"({self.error}, retrying {self.retry_count} /"
                f" {self.max_retry})"
                if self.retry_count > 0
                else ""
            )
            return f"{self.url} {retry}"

    def __hash__(self):
        return hash(self.url)

    def __eq__(self, other: Request) -> bool:
        return self.url == other.url
