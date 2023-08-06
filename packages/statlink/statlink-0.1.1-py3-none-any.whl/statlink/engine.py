from __future__ import annotations
import asyncio
from contextlib import asynccontextmanager
from abc import ABC, abstractmethod

import aiohttp
from playwright import async_api as playwright

from .request import (
    Request,
    RequestError,
    RequestTimeoutError,
    RequestConnectionError
)
from .response import Response


class Engine(ABC):

    name = None

    @abstractmethod
    async def fetch(self, request: "Request") -> Response:
        ...

    @classmethod
    @abstractmethod
    @asynccontextmanager
    async def get(cls) -> Engine:
        ...


class AioHTTPEngine(Engine):

    name = "aiohttp"

    def __init__(self):
        conn = aiohttp.TCPConnector(limit_per_host=20, limit=30)
        self.client_session = aiohttp.ClientSession(connector=conn)

    @classmethod
    @asynccontextmanager
    async def get(cls) -> AioHTTPEngine:
        engine = cls()
        async with engine.client_session:
            yield engine

    async def fetch(self, request: "Request") -> Response:
        try:
            async with self.client_session.get(
                request.url, timeout=request.timeout
            ) as client_response:
                response_text = None
                if client_response.charset:
                    try:
                        response_text = await client_response.text()
                    except ValueError:
                        pass
                if not response_text:
                    await client_response.read()
                return Response(
                    text=response_text,
                    status=client_response.status
                )
        except asyncio.TimeoutError:
            raise RequestTimeoutError()
        except aiohttp.ClientConnectionError as exc:
            raise RequestConnectionError(exc)
        except Exception as exc:
            raise RequestError(exc)


class BrowserEngine(Engine, ABC):
    def __init__(self):
        self.browser = None

    @classmethod
    @asynccontextmanager
    async def get(cls) -> BrowserEngine:
        engine = cls()
        async with playwright.async_playwright() as p:
            engine.browser = await getattr(p, cls.name).launch()
            yield engine

    async def fetch(self, request: "Request") -> Response:
        page = await self.browser.new_page()
        try:
            response = await page.goto(
                request.url,
                timeout=request.timeout * 1000,
                wait_until="domcontentloaded"
            )

            return Response(
                text=await page.content(),
                status=response.status
            )

        except playwright.TimeoutError:
            raise RequestTimeoutError()

        except playwright.Error as exc:
            error_message = str(exc).lower()
            connection_error_messages = [
                "err_name_not_resolved",
                "err_address_unreachable"
            ]
            if any(
                message in error_message
                for message in connection_error_messages
            ):
                raise RequestConnectionError()
            raise RequestError(self._truncate_error(str(exc)))

        except Exception as exc:
            raise RequestError(exc)

        finally:
            await page.close()

    @staticmethod
    def _truncate_error(error_message: str) -> str:
        return error_message.split("\n=", maxsplit=1)[0].capitalize()


class ChromiumEngine(BrowserEngine):
    name = "chromium"


class FirefoxEngine(BrowserEngine):
    name = "firefox"


class WebKitEngine(BrowserEngine):
    name = "webkit"


ENGINE_MAPPING = {
    engine_class.name: engine_class
    for engine_class in [
        AioHTTPEngine,
        ChromiumEngine,
        FirefoxEngine,
        WebKitEngine,
    ]
}
