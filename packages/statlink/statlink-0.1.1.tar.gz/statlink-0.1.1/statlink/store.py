from dataclasses import dataclass, field
from itertools import groupby
from collections import defaultdict

from .request import Request, RequestState


@dataclass
class CountByState:
    not_started: int = 0
    in_progress: int = 0
    success: int = 0
    error: int = 0
    remaining: int = field(init=False)
    completed: int = field(init=False)
    total: int = field(init=False)

    def __post_init__(self):
        self.completed = self.success + self.error
        self.remaining = self.not_started + self.in_progress
        self.total = self.not_started + self.in_progress + self.completed


class Store:
    def __init__(self):
        self._requests = {}
        self._links = defaultdict(list)

    def add_request(self, request: Request):
        self._requests[request.url] = request

    def add_link(self, url: str, parent: str):
        self._links[url].append(parent)

    def get_request(self, url: str) -> Request:
        return self._requests.get(url)

    def get_requests_in_progress(self) -> list[Request]:
        return self._get_requests(RequestState.IN_PROGRESS)

    def get_requests_completed(self) -> list[Request]:
        return self._get_requests(RequestState.SUCCESS, RequestState.ERROR)

    def get_requests_error(self) -> list[Request]:
        return self._get_requests(RequestState.ERROR)

    def count_links_by_request_state(self) -> CountByState:
        return CountByState(
            **{
                state_name: sum(
                    len(self._links[request.url]) for request in requests
                )
                for state_name, requests in self._get_requests_by_state().items()
            }
        )

    def _get_requests(self, *state: RequestState) -> list[Request]:
        return [
            request
            for request in self._requests.values()
            if request.state in state
        ]

    def _get_requests_by_state(self) -> dict[str, list[Request]]:
        return {
            state.name.lower(): list(requests_iter)
            for state, requests_iter in groupby(
                sorted(self._requests.values(), key=lambda r: r.state),
                key=lambda r: r.state,
            )
        }
