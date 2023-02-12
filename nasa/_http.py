from __future__ import annotations
from typing import ClassVar, Any

import requests
import sys
import asyncio
from asyncio import AbstractEventLoop

import aiohttp
from aiohttp.client_exceptions import ContentTypeError


class Route:
    BASE_API_URL: ClassVar[str] = "https://api.nasa.gov"

    def __init__(self, method: str, path: str) -> None:
        self.path = path
        self.method = method
        self.url = self.BASE_API_URL + self.path


class _BaseHTTPClient:
    """The base HTTPClient."""
    _user_agent: str = f"Nasa.py 0.0.1a (GitHub here) Python/{sys.version_info[0]}.{sys.version_info[1]} requests/{requests.__version__}"


class HTTPClient(_BaseHTTPClient):
    def __init__(self, *, token: str | None = None) -> None:
        self.__token = token

    def request(
        self,
        *,
        route: Route,
        params: dict[str, Any] = {}
    ) -> Any:
        headers: dict[str, str] = {
            "User-Agent": self._user_agent,
        }
        if not self.__token:
            raise # add token exception here

        params["api_key"] = self.__token
        response = requests.request(method=route.method, headers=headers, params=params, url=route.url)

        try:
            return response.json()
        except:
            return response
    
    @staticmethod
    def get_image_as_bytes(url: str) -> bytes:
        if not url:
            return b""
        return (requests.request(method="GET", url=url)).content
        

class AsyncHTTPClient(_BaseHTTPClient):
    def __init__(
        self,
        *,
        loop: AbstractEventLoop | None = None,
        token: str | None = None,
        session: aiohttp.ClientSession | None = None
    ) -> None:
        self._loop = loop or asyncio.get_event_loop()
        self.__token = token
        self._session = session or aiohttp.ClientSession(trust_env=True)
    
    @property
    def is_closed(self) -> bool:
        return self._session.closed

    async def request(
        self,
        *,
        route: Route,
        params: dict[str, Any] = {}
    ) -> Any:
        headers: dict[str, str] = {
            "User-Agent": self._user_agent,
        }

        if not self.__token:
            raise # token exc here

        params["api_key"] = self.__token
        async with self._session.request(route.method, route.url, params=params, ssl=False, headers=headers) as resp:
            try:
                content = await resp.json()
            except ContentTypeError:
                content = await resp.text()
            return content



        #self._loop.create_task(self._session.close(), name="Session closer") #i should close the session only when there's an exception
        # or when there's a keyboard interrupt also if the session obj was provided by the user i should not close it
        # the user should handle it himself (i'll provide a method called close() to close a session)

    async def close(self) -> None:
        """Closes the aiohttp.ClientSession session"""
        await self._session.close()

    @staticmethod
    async def get_image_as_bytes(url: str) -> bytes:
        if not url:
            return b""
        async with aiohttp.request("GET", url=url) as resp:
            return await resp.read()