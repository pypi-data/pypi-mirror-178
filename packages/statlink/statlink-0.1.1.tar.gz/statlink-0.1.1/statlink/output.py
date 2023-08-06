import asyncio
from time import time

from rich.console import Console, Control
from rich.spinner import Spinner
from rich.control import ControlType
from rich.live import Live
from rich.console import ConsoleRenderable, RenderResult, ConsoleOptions


from .request import Request
from .store import Store


class InProgressRequests(ConsoleRenderable):
    def __init__(self, store: Store, max_lines: int = 3):
        self.store = store
        self.max_lines = max_lines
        self.spinners = {}

    def get_spinner(self, request: Request) -> Spinner:
        if request.url not in self.spinners:
            self.spinners[request.url] = Spinner(name="dots")

        spinner = self.spinners[request.url]
        spinner.text = request.result()
        return spinner

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        in_progress_requests = self.store.get_requests_in_progress()
        for in_progress_request in in_progress_requests[: self.max_lines]:
            yield self.get_spinner(in_progress_request)

        # Clean old spinners
        in_progress_request_urls = [
            request.url for request in in_progress_requests
        ]
        for url in list(self.spinners.keys()):
            if url not in in_progress_request_urls:
                del self.spinners[url]


class StatusBar(ConsoleRenderable):
    def __init__(self, store: Store):
        self.store = store
        self.start_time = time()

    def elapsed_time(self):
        return time() - self.start_time

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        status = self.store.count_links_by_request_state()
        yield (
            f"In progress: {status.in_progress} "
            f"| Success: {status.success} "
            f"| Failed: {status.error} "
            f"| Remaining: {status.remaining} "
            f"| Total: {status.total} "
            f"| Elapsed time: {self.elapsed_time():.1f}s"
        )


class RenderablesContainer(ConsoleRenderable):
    def __init__(self, renderables: list[ConsoleRenderable]):
        self.renderables = renderables

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        for renderable in self.renderables:
            for render_result in renderable.__rich_console__(
                console=console, options=options
            ):
                yield render_result


class Output:
    def __init__(
        self,
        store: Store,
        in_progress_display: int = 3,
        status_bar: bool = True,
    ):
        self.console = Console()
        self.store = store
        self.status_bar = status_bar
        self.requests_displayed = []
        self.renderables = []

        if in_progress_display > 0:
            self.renderables.append(
                InProgressRequests(store=store, max_lines=in_progress_display)
            )
        if status_bar:
            self.renderables.append(StatusBar(store=store))

    async def start(self):
        try:
            self.console.show_cursor(False)
            with Live(
                console=self.console,
                renderable=RenderablesContainer(renderables=self.renderables),
                auto_refresh=False,
                transient=True,
            ) as live:
                while True:
                    self.display_completed_requests()
                    live.refresh()
                    await asyncio.sleep(0.05)

        except asyncio.CancelledError:
            self.console.show_cursor(True)
            raise

    def display_completed_requests(self):
        for request in self.store.get_requests_completed():
            if request not in self.requests_displayed:
                self.console.print(
                    request.result(),
                    end=f"{Control((ControlType.ERASE_IN_LINE, 0))}\n",
                )
            self.requests_displayed.append(request)
