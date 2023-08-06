import typing
import asyncio
from signal import SIGINT, SIGTERM
from urllib.parse import urlparse
from concurrent.futures.thread import ThreadPoolExecutor

from .source import Source, HTMLSource
from .request import Request
from .output import Output
from .store import Store
from .engine import ENGINE_MAPPING, Engine


DEFAULT_CONCURRENCY = 20
DEFAULT_DEPTH = -1
DEFAULT_TIMEOUT = 20
DEFAULT_ENGINE = "aiohttp"
DEFAULT_MAX_RETRY = 1


class Crawler:
    def __init__(
        self,
        concurrency: int = DEFAULT_CONCURRENCY,
        depth: int = DEFAULT_DEPTH,
        timeout: int = DEFAULT_TIMEOUT,
        max_retry: int = DEFAULT_MAX_RETRY,
        engine: str = DEFAULT_ENGINE,
        url_filters: list[str] | None = None,
        loop=None,
    ):
        self.loop = loop or asyncio.get_event_loop()
        self.concurrency = concurrency
        self.depth = depth
        self.timeout = timeout
        self.max_retry = max_retry
        self.url_filters = url_filters or []
        self.store = Store()
        self.output = Output(store=self.store)
        self.requests_queue = asyncio.Queue()
        self.tasks = None
        self.add_source_executor = ThreadPoolExecutor(max_workers=concurrency)
        self.source_queue = asyncio.Queue()
        self.engine_class = ENGINE_MAPPING.get(engine)

    def start(self):
        for signal in (SIGINT, SIGTERM):
            self.loop.add_signal_handler(
                signal, lambda: asyncio.create_task(self.stop())
            )
        try:
            self.loop.run_until_complete(self._async_start())
        finally:
            self.display_result()

    async def _async_start(self):
        async with self.engine_class.get() as engine:
            request_workers = [
                self._request_worker(engine) for _ in range(self.concurrency)
            ]
            add_source_workers = [
                self._add_source_worker() for _ in range(self.concurrency)
            ]
            self.tasks = [
                asyncio.create_task(coro)
                for coro in [
                    *request_workers,
                    *add_source_workers,
                    self.output.start(),
                    self.requests_queue.join(),
                ]
            ]
            # Here we wait for the requests manager to have no more requests
            # to process and for other tasks to capture inner tasks
            # exceptions different from asyncio.CancelledError
            while not (
                self.source_queue.empty() and self.requests_queue.empty()
            ):
                done, pending = await asyncio.wait(
                    self.tasks, return_when=asyncio.FIRST_COMPLETED
                )
                if any(task.cancelled() for task in done):
                    break

            for task in done:
                if not task.cancelled():
                    if exc := task.exception():
                        raise exc
            await self.stop(tasks=pending)

    async def stop(self, tasks: typing.Optional[set[asyncio.Task]] = None):
        tasks = tasks or self.tasks
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

    def add_source(self, source: Source, filter_domains: bool = True):
        for url in source.find_urls():
            self.add_url(
                url=url,
                filter_domain=filter_domains,
                parent=source.url,
                depth=source.depth,
            )

    def add_url(
        self,
        url: str,
        filter_domain: bool = True,
        parent: str | None = None,
        depth: int = 0,
    ):
        if not self.store.get_request(url=url):
            request = Request(
                url=url,
                depth=depth,
                timeout=self.timeout,
                max_retry=self.max_retry
            )
            self.store.add_request(request)
            self.requests_queue.put_nowait(request)

        self.store.add_link(url=url, parent=parent)

        if filter_domain:
            self.url_filters.append(urlparse(url).netloc)

    async def _request_worker(self, engine: Engine):
        while True:
            request = await self.requests_queue.get()
            response = await request.fetch(engine)
            if response and response.text and (
                self.depth < 0 or request.depth < self.depth
            ):
                source = HTMLSource(
                    content=response.text,
                    url_filters=self.url_filters,
                    url=request.url,
                    depth=request.depth + 1,
                )
                if self.requests_queue.qsize() == 0:
                    self.add_source(source)
                else:
                    self.source_queue.put_nowait(source)

            self.requests_queue.task_done()

    async def _add_source_worker(self):
        while True:
            source = await self.source_queue.get()
            await self.loop.run_in_executor(
                self.add_source_executor, self.add_source, source, False
            )
            self.source_queue.task_done()

    def display_result(self):
        print(self.store.count_links_by_request_state(), end=f"\x1b[0K\n")
        error_requests = self.store.get_requests_error()
        if error_requests:
            print(f"Failed requests:", end=f"\x1b[0K\n")
            for request in error_requests:
                print(request.result(), end=f"\x1b[0K\n")
