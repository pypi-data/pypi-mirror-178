import click

from .source import Source
from .crawler import (
    Crawler,
    DEFAULT_CONCURRENCY,
    DEFAULT_DEPTH,
    DEFAULT_TIMEOUT,
    DEFAULT_ENGINE,
    DEFAULT_MAX_RETRY
)
from .utils import is_url


@click.command(no_args_is_help=True)
@click.argument("sources", nargs=-1)
@click.option(
    "--concurrency",
    "-c",
    default=DEFAULT_CONCURRENCY,
    show_default=True,
    type=int,
    help="Set the maximum number of concurrent requests.",
)
@click.option(
    "--allow-external",
    is_flag=True,
    show_default=True,
    help="Allow external URL to be checked.",
)
@click.option(
    "--depth",
    "-d",
    default=DEFAULT_DEPTH,
    show_default=True,
    type=int,
    help="Recursion depth value for checking URLs, "
    "negative value will set it to infinity.",
)
@click.option(
    "--timeout",
    "-t",
    default=DEFAULT_TIMEOUT,
    show_default=True,
    type=int,
    help="Set timeout for each requests.",
)
@click.option(
    "--max-retry",
    "-r",
    default=DEFAULT_MAX_RETRY,
    show_default=True,
    type=int,
    help="Set the maximum number of time a request will be retried if failed"
)
@click.option(
    "--engine",
    default=DEFAULT_ENGINE,
    show_default=True,
    type=click.Choice(["aiohttp", "chromium", "firefox", "webkit"]),
    help="Engine that will be used to make requests.",
)
def main(
    sources: tuple[str],
    concurrency: int,
    allow_external: bool,
    depth: int,
    timeout: int,
    max_retry: int,
    engine: str,
):
    Command(
        sources=list(sources),
        concurrency=concurrency,
        allow_external=allow_external,
        depth=depth,
        timeout=timeout,
        max_retry=max_retry,
        engine=engine,
    ).run()


class Command:
    def __init__(
        self,
        sources: list[str],
        concurrency: int,
        allow_external: bool,
        depth: int,
        timeout: int,
        max_retry: int,
        engine: str,
    ):
        self.crawler = Crawler(
            concurrency=concurrency,
            depth=depth,
            timeout=timeout,
            max_retry=max_retry,
            engine=engine,
        )
        for source in sources:
            if is_url(source):
                self.crawler.add_url(
                    url=source, filter_domain=not allow_external
                )
            else:
                for source_inst in Source.from_path(path=source):
                    self.crawler.add_source(
                        source=source_inst, filter_domains=not allow_external
                    )

    def run(self):
        self.crawler.start()
