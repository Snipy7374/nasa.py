from __future__ import annotations
from typing import overload, TYPE_CHECKING, Union
from typing_extensions import TypeAlias

import os
import io

import aiofiles

if TYPE_CHECKING:
    from ._http import HTTPClient, AsyncHTTPClient

__all__: tuple[str, ...] = (
    "AsyncAsset",
    "SyncAsset",
)

# recreating the returned type of the file.name property of aiofiles
# bad typing on their end
StrOrBytes: TypeAlias = Union[str, bytes, os.PathLike[str], os.PathLike[bytes]] 
# if i want to support python versions < 3.10 i need Union here


class _BaseAsset:
    _url: str
    _bytes: bytes | None = None

    def __len__(self) -> int:
        return len(self._url)

    def __str__(self) -> str:
        return self._url

    def __hash__(self) -> int:
        return hash(self._url)
    
    @property
    def url(self) -> str:
        return self._url
    


class AsyncAsset(_BaseAsset):
    def __init__(self, url: str, http_client: AsyncHTTPClient) -> None:
        self._url = url
        self.__http = http_client

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, AsyncAsset) and self._url == __o.url

    def __repr__(self) -> str:
        return f"AsyncAsset(url={self._url!r})"

    async def read(self) -> bytes:
        self._bytes = await self.__http.get_image_as_bytes(self._url)
        return self._bytes
    
    @property
    def bytes_asset(self) -> bytes | None:
        # i can't do the same thing as the SyncAsset
        # coz properties are syncronous so this property
        # could return None, if it return None then it means that the bytes
        # aren't cached yet so the user needs to call read(), that is
        # an API call tough the X-ratelimit-requests will not be
        # affected since it doesn't use the API key
        return self._bytes

    @overload
    async def save(
        self,
        file: io.BufferedIOBase,
        *,
        seek_at_end: bool = ...
    ) -> int:
        ...
    
    @overload
    async def save(
        self,
        file: str | bytes | os.PathLike,
        *,
        seek_at_end: bool = ...
    ) -> StrOrBytes:
        ...

    async def save(
        self,
        file: str | bytes | os.PathLike | io.BufferedIOBase,
        *,
        seek_at_end: bool = True
    ) -> int | StrOrBytes:
        content = self._bytes if self._bytes else await self.read()
        if isinstance(file, io.BufferedIOBase):
            written = file.write(content)
            if seek_at_end:
                file.seek(0)
            return written
        else:
            async with aiofiles.open(file, "wb") as f:
                await f.write(content)
            return f.name

class SyncAsset(_BaseAsset):
    def __init__(self, url: str, http_client: HTTPClient) -> None:
        self._url = url
        self.__http = http_client

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, SyncAsset) and self._url == __o.url
    
    def __repr__(self) -> str:
        return f"SyncAsset(url={self._url!r})"

    def read(self) -> bytes:
        self._bytes = self.__http.get_image_as_bytes(self._url)
        return self._bytes
    
    @property
    def bytes_asset(self) -> bytes:
        if not self._bytes:
            return self.read()
        return self._bytes

    @overload
    def save(
        self,
        file: str | bytes | os.PathLike,
        *,
        seek_at_end: bool = ...
    ) -> str:
        ...

    @overload
    def save(
        self,
        file: io.BufferedIOBase,
        *,
        seek_at_end: bool = ...
    ) -> int:
        ...

    def save(
        self,
        file: str | bytes | os.PathLike | io.BufferedIOBase,
        *,
        seek_at_end: bool = True
    ) -> int | str:
        content = self._bytes if self._bytes else self.read()
        if isinstance(file, io.BufferedIOBase):
            written = file.write(content)
            if seek_at_end:
                file.seek(0)
            return written
        else:
            with open(file, "wb") as f:
                f.write(content)
            return f.name