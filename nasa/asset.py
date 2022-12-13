from __future__ import annotations
from typing import overload, TYPE_CHECKING

import os
import io

if TYPE_CHECKING:
    from ._http import HTTPClient

__all__: tuple[str, ...] = (
    "AsyncAsset",
    "SyncAsset",
)


class AsyncAsset:
    __slot__: tuple[str, ...] = (
        "_url",
    )

    def __init__(self, url: str, http_client: HTTPClient) -> None:
        self._url = url
        self.__http = http_client

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, AsyncAsset) and self._url == __o.url

    def __len__(self) -> int:
        return len(self._url)

    def __repr__(self) -> str:
        return f"AsyncAsset(url={self._url!r})"

    def __str__(self) -> str:
        return self._url

    def __hash__(self) -> int:
        return hash(self._url)

    @property
    def url(self) -> str:
        return self._url

    async def read(self) -> bytes: # still need to work on the async part
        raise NotImplementedError

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
    ) -> str:
        ...

    async def save(
        self,
        file: str | bytes | os.PathLike | io.BufferedIOBase,
        *,
        seek_at_end: bool = True
    ) -> int | str: # still need to work on the async part
        raise NotImplementedError


class SyncAsset:
    __slot__: tuple[str, ...] = (
        "_url",
    )

    def __init__(self, url: str, http_client: HTTPClient) -> None:
        self._url = url
        self.__http = http_client

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, SyncAsset) and self._url == __o.url
    
    def __len__(self) -> int:
        return len(self._url)
    
    def __repr__(self) -> str:
        return f"SyncAsset(url={self._url!r})"
    
    def __str__(self) -> str:
        return self._url
    
    def __hash__(self) -> int:
        return hash(self._url)
    
    @property
    def url(self) -> str:
        return self._url

    def read(self) -> bytes:
        return self.__http.get_image_as_bytes(self.url)

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
        content = self.read()
        if isinstance(file, io.BufferedIOBase):
            written = file.write(content)
            if seek_at_end:
                file.seek(0)
            return written
        else:
            with open(file, "wb") as f:
                f.write(content)
            return f.name