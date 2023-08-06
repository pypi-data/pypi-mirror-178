from __future__ import annotations

from pathlib import Path
from urllib.parse import urldefrag
from contextlib import suppress

from lxml.html import document_fromstring
from lxml.etree import ParserError

from .utils import URL_RE_MULTI


class Source:
    def __init__(
        self,
        content: str,
        url_filters: list[str] | None = None,
        url: str | None = None,
        depth: int = 0,
    ):
        self.content = content
        self.url_filters = url_filters
        self.url = url
        self.depth = depth

    @classmethod
    def from_path(cls, path: str, recursive: bool = False) -> list[Source]:
        file_paths = []
        sources = []
        path = Path(path).resolve()
        glob = ""
        while not path.exists():
            path, glob = path.parent, Path(path.name) / glob

        if path.is_dir():
            glob_pattern = glob or ("**/*" if recursive else "*")
            file_paths = sorted(
                [path for path in path.glob(glob_pattern) if path.is_file()]
            )
        elif path.is_file():
            file_paths = [path]

        for path in file_paths:
            with open(path) as f:
                sources.append(cls(f.read()))

        return sources

    def find_urls(self) -> list[str]:
        return [
            urldefrag(url)[0]
            for url in URL_RE_MULTI.findall(self.content)
            if not self.url_filters
            or any([url_filter in url for url_filter in self.url_filters])
        ]


class HTMLSource(Source):
    def find_urls(self):
        with suppress(ValueError, ParserError):
            tree = document_fromstring(self.content)
            tree.make_links_absolute(self.url)
            return [
                urldefrag(url[2])[0]
                for url in tree.iterlinks()
                if not self.url_filters
                or any(
                    [
                        url_filter in urldefrag(url[2])[0]
                        for url_filter in self.url_filters
                    ]
                )
            ]
        return []
