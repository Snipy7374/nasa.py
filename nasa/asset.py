from __future__ import annotations
from typing import overload, TYPE_CHECKING, Union
from typing_extensions import TypeAlias

import os
import io
import logging

import aiofiles

from .enums import FileTypes

if TYPE_CHECKING:
    from ._http import HTTPClient, AsyncHTTPClient

__all__: tuple[str, ...] = (
    "AsyncAsset",
    "SyncAsset",
)

_log = logging.getLogger(__name__)

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
        """:class:`str`: The url of the asset."""
        return self._url
    


class AsyncAsset(_BaseAsset):
    """Represents an asset returned by the NASA Api as a python object.
    
    Supported Operations

        .. container:: operations

            .. describe:: x == y

                Checks if two Assets holds the same file.
        
            .. describe:: x != y

                Checks if two Assets don't holds the same file.

    .. versionadded:: 0.0.1
    """
    def __init__(self, url: str, http_client: AsyncHTTPClient, url_state: str) -> None:
        self._url = url
        self.__http = http_client
        self.__url_state = url_state

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, AsyncAsset) and self._url == __o.url

    def __repr__(self) -> str:
        return f"AsyncAsset(url={self._url!r})"

    async def read(self) -> bytes:
        """Fetch the file and return its bytes.
        
        .. note::
            This function doesn't use the token. As a result requests
            made with this method won't reduce your request counter.

        Returns
        -------
        :class:`bytes`
            The ``bytes`` of the file.
        """
        _log.info("Getting bytes of %s", self._url)
        self._bytes = await self.__http.get_image_as_bytes(self._url)
        return self._bytes
    
    @property
    def bytes_asset(self) -> bytes | None:
        """Union[:class:`bytes`, ``None``]: the bytes of the asset if 
        already cached otherwise ``None``.
        
        .. hint::
            This property can be ``None`` if the Asset wasn't previously fetched.
            You should check if ``bytes_asset`` is ``None`` and then fetch it.
            Check the example at :attr:`AstronomyPicture.image`.
        """
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
        file: str | bytes | os.PathLike[str],
        *,
        seek_at_end: bool = ...
    ) -> StrOrBytes:
        ...

    async def save(
        self,
        file: str | bytes | os.PathLike[str] | io.BufferedIOBase,
        *,
        seek_at_end: bool = True
    ) -> int | StrOrBytes:
        """Saves the Asset locally. If ``file`` is ``io.BufferedIOBase`` returns the
        numbers of bytes writed otherwise the name of the file or the path where
        it was saved.

        Parameters
        ----------
        file: Union[:class:`str`, :class:`bytes`, :class:`os.PathLike`, :class:`io.BufferedIOBase`]
        seek_at_end: :class:`bool`

        Returns
        -------
        Union[:class:`int`, :class:`str`, :class:`bytes`, :class:`os.PathLike`]
            If ``file`` is :class:`io.BufferedIOBase` the number of bytes written; otherwise
            the name of the file or the path where it was saved.
        """
        content = self._bytes if self._bytes else await self.read()
        if isinstance(file, io.BufferedIOBase):
            written = file.write(content)
            if seek_at_end:
                file.seek(0)
            return written
        else:
            async with aiofiles.open(file, "wb") as f:
                await f.write(content)
            _log.info("Asset was saved at %s", f.name)
            return f.name


class SyncAsset(_BaseAsset):
    """Represents an asset returned by the NASA Api as a python object.
    
    Supported Operations

        .. container:: operations

            .. describe:: x == y

                Checks if two Assets holds the same file.
        
            .. describe:: x != y

                Checks if two Assets don't holds the same file.

    .. versionadded:: 0.0.1
    """
    def __init__(self, url: str, http_client: HTTPClient, url_state: str) -> None:
        self._url = url
        self.__http = http_client
        self.__url_state = url_state

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, SyncAsset) and self._url == __o.url
    
    def __repr__(self) -> str:
        return f"SyncAsset(url={self._url!r})"

    def read(self, asset_as = None) -> bytes:
        """Fetch the file and return its bytes.
        
        .. note::
            This function doesn't use the token. As a result requests
            made with this method won't reduce your request counter.

        Returns
        -------
        :class:`bytes`
            The ``bytes`` of the file.
        """
        _log.info("Getting bytes of %s", self._url)
        if self.__url_state == "partial":
            if not isinstance(asset_as, FileTypes):
                raise ValueError
            self._url = self._url.format(asset_as, asset_as)
        self._bytes = self.__http.get_image_as_bytes(self._url)
        return self._bytes
    
    @property
    def bytes_asset(self) -> bytes:
        """Union[:class:`bytes`, ``None``]: The bytes of the asset if 
        already cached otherwise ``None``.
        
        .. hint::
            This property can be ``None`` if the Asset wasn't previously fetched.
            You should check if ``bytes_asset`` is ``None`` and then fetch it.
            Check the example at :attr:`AstronomyPicture.image`.
        """
        if not self._bytes:
            return self.read()
        return self._bytes

    @overload
    def save(
        self,
        file: str | bytes | os.PathLike[str],
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
        file: str | bytes | os.PathLike[str] | io.BufferedIOBase,
        *,
        seek_at_end: bool = True
    ) -> int | str:
        """Saves the Asset locally. If ``file`` is ``io.BufferedIOBase`` returns the
        numbers of bytes writed otherwise the name of the file or the path where
        it was saved.

        Parameters
        ----------
        file: Union[:class:`str`, :class:`bytes`, :class:`os.PathLike`, :class:`io.BufferedIOBase`]
        seek_at_end: :class:`bool`

        Returns
        -------
        Union[:class:`int`, :class:`str`]
            If ``file`` is :class:`io.BufferedIOBase` the number of bytes written; otherwise
            the name of the file or the path where it was saved.
        """
        content = self._bytes if self._bytes else self.read()
        if isinstance(file, io.BufferedIOBase):
            written = file.write(content)
            if seek_at_end:
                file.seek(0)
            return written
        else:
            with open(file, "wb") as f:
                f.write(content)
            _log.info("Asset was saved at %s", f.name)
            return f.name